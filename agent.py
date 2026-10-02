import json
import re
import sys
import time

from llm import LLMError
from relevance import judge_relevance
from prompts import (PLANNING_SYSTEM, REACT_SYSTEM, planning_user,
                     react_user_intro)
from trace import Step, Trace, now_iso


def extract_json(text):
    if text is None:
        raise ValueError("empty LLM response")
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\n?", "", t)
        t = re.sub(r"\n?```$", "", t).strip()
    start = t.find("{")
    end = t.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"no JSON object found in: {text[:200]}")
    blob = t[start:end + 1]
    try:
        return json.loads(blob)
    except json.JSONDecodeError:
        repaired = re.sub(r",(\s*[}\]])", r"\1", blob)
        repaired = re.sub(r'(".*?"|true|false|null|-?\d+(?:\.\d+)?)(\s*\n\s*)(")',
                          r"\1,\2\3", repaired)
        return json.loads(repaired)


GROUNDING_ACTIONS = {"search", "get_sections", "read_section"}


class Task:
    def __init__(self, question, stop_criterion=None, language="en", gold=None):
        self.question = question
        self.stop_criterion = stop_criterion
        self.language = language
        self.gold = gold


class DeepResearchAgent:
    def __init__(self, llm, wiki, config):
        self.llm = llm
        self.wiki = wiki
        self.cfg = config

    def _plan(self, task):
        msgs = [{"role": "system", "content": PLANNING_SYSTEM},
                {"role": "user",
                 "content": planning_user(task.question, task.stop_criterion)}]
        try:
            data = extract_json(self.llm.chat(msgs, force_json=self.cfg.force_json))
        except Exception:
            data = {}
        sub = data.get("sub_questions", []) or []
        plan = data.get("plan", "") or ""
        if task.stop_criterion:
            stop, source = task.stop_criterion, "provided by user"
        else:
            stop = (data.get("stop_criterion", "") or
                    "Enough evidence has been read from Wikipedia to answer the question unambiguously.")
            source = "proposed by agent"
        return sub, plan, stop, source

    def _has_grounded(self, trace):
        return any(s.action == "read_section" and not s.observation.startswith("Tool error")
                   for s in trace.steps)

    def _collect_observations(self, trace):
        return [s.observation for s in trace.steps
                if s.action == "read_section" and not s.observation.startswith("Tool error")]

    def _apply_relevance_gate(self, trace, answer, suff):
        if not (self.cfg.relevance_gate and suff.get("met")):
            return suff
        observations = self._collect_observations(trace)
        supported, reasoning = judge_relevance(self.llm.chat, extract_json,
                                               trace.question, answer, observations)
        trace.relevance_checked = True
        if not supported:
            return {"met": False, "confidence": 0.0,
                   "justification": f"Overridden by relevance gate: {reasoning}"}
        return suff

    def _dispatch(self, action, ai, sources, lang_default):
        lang = ai.get("lang") or lang_default
        if action == "search":
            res = self.wiki.search(ai.get("query", ""),
                                   limit=self.cfg.search_limit, lang=lang)
            if not res:
                return "No results."
            return "\n".join(f"- {r['title']}: {r['snippet']}" for r in res)
        if action == "get_sections":
            data = self.wiki.get_sections(ai.get("title", ""), lang=lang)
            lines = [f"[{s['index']}] {s['line']}" for s in data["sections"]]
            return f"Sections of '{data['title']}':\n" + "\n".join(lines)
        if action == "read_section":
            title = ai.get("title", "")
            section = str(ai.get("section", "0"))
            data = self.wiki.read_section(title, section=section, lang=lang,
                                          char_limit=self.cfg.obs_char_limit)
            url = (f"https://{lang}.wikipedia.org/wiki/"
                   + data["title"].replace(" ", "_"))
            requested_title = data.get("requested_title", title)
            redirected = data.get("redirected", False)
            src = {"lang": lang, "title": data["title"], "requested_title": requested_title,
                  "redirected": redirected, "section": section, "url": url}
            if src not in sources:
                sources.append(src)
            suffix = " [truncated]" if data["truncated"] else ""
            redirect_note = (f" [redirected from requested '{requested_title}']"
                             if redirected else "")
            body = data["text"] or "(empty section)"
            return f"{data['title']}{redirect_note} — section {section}{suffix}:\n{body}"
        raise ValueError(f"unknown action '{action}'")

    def run(self, task):
        t0 = time.time()
        trace = Trace(question=task.question, language=task.language,
                      backend=self.cfg.backend, model=self.cfg.model,
                      started_at=now_iso())
        sub, plan, stop, source = self._plan(task)
        trace.sub_questions, trace.plan = sub, plan
        trace.stop_criterion, trace.stop_criterion_source = stop, source

        messages = [{"role": "system", "content": REACT_SYSTEM},
                    {"role": "user",
                     "content": react_user_intro(task.question, sub, stop, task.language)}]
        sources = []
        n = 0
        finished = False
        consecutive_llm_failures = 0
        max_consecutive_llm_failures = 3
        aborted_on_llm_failures = False
        while n < self.cfg.max_steps:
            print(f"  step {n + 1}/{self.cfg.max_steps}: calling LLM...", file=sys.stderr, flush=True)
            try:
                raw = self.llm.chat(messages, force_json=self.cfg.force_json)
                consecutive_llm_failures = 0
            except LLMError as e:
                consecutive_llm_failures += 1
                trace.steps.append(Step(n=n + 1, thought="(LLM call failed)",
                                        action="_error", observation=str(e)))
                if consecutive_llm_failures >= max_consecutive_llm_failures:
                    trace.stopped_reason = (f"aborted after {consecutive_llm_failures} "
                                            f"consecutive LLM call failures: {e}")
                    aborted_on_llm_failures = True
                    break
                messages.append({"role": "user",
                                 "content": "Your previous response could not be generated "
                                            "(the API call failed). Respond again with EXACTLY "
                                            "ONE JSON object, keeping it concise."})
                continue
            act = None
            last_parse_error = None
            for parse_attempt in range(3):
                try:
                    act = extract_json(raw)
                    break
                except Exception as e:
                    last_parse_error = e
                    messages.append({"role": "assistant", "content": raw})
                    messages.append({"role": "user",
                                     "content": f"Your last message was not valid JSON ({e}). "
                                                f"Respond again with EXACTLY ONE JSON object only."})
                    if parse_attempt == 2:
                        break
                    try:
                        raw = self.llm.chat(messages, force_json=self.cfg.force_json)
                    except LLMError as e2:
                        last_parse_error = e2
                        raw = ""
                        break

            n += 1
            if act is None:
                trace.steps.append(Step(n=n, thought="(unparseable output)",
                                        action="_error",
                                        observation=f"unparseable after retries: {last_parse_error}"))
                continue
            step = Step(n=n, thought=act.get("thought", ""),
                        action=act.get("action", ""),
                        action_input=act.get("action_input", {}) or {},
                        sufficiency_note=act.get("sufficiency_note", ""))
            if step.action == "finish":
                if not self._has_grounded(trace) and n < self.cfg.max_steps:
                    step.observation = ("Rejected: you must call read_section at least once "
                                        "before finish. search/get_sections alone are not evidence.")
                    trace.steps.append(step)
                    messages.append({"role": "assistant", "content": raw})
                    messages.append({"role": "user", "content": step.observation})
                    continue
                trace.final_answer = step.action_input.get("answer", "")
                suff = step.action_input.get("sufficiency", {}) or {}
                grounded = self._has_grounded(trace)
                if not grounded:
                    suff = {"met": False, "confidence": 0.0,
                            "justification": "Overridden: finish accepted at step budget "
                                             "with no Wikipedia section ever read."}
                else:
                    suff = self._apply_relevance_gate(trace, trace.final_answer, suff)
                trace.sufficiency = suff
                step.observation = ("(finished)" if grounded
                                    else "(finished ungrounded; sufficiency overridden to false)")
                trace.steps.append(step)
                finished = True
                trace.voluntary_finish = grounded
                trace.stopped_reason = "agent called finish"
                break
            print(f"  step {n}/{self.cfg.max_steps}: {step.action} {step.action_input}",
                 file=sys.stderr, flush=True)
            try:
                obs = self._dispatch(step.action, step.action_input, sources, task.language)
            except Exception as e:
                obs = f"Tool error: {e}"
            if len(obs) > self.cfg.obs_char_limit:
                obs = obs[:self.cfg.obs_char_limit] + " [truncated]"
            step.observation = obs
            trace.steps.append(step)
            messages.append({"role": "assistant", "content": raw})
            messages.append({"role": "user", "content": f"Observation:\n{obs}"})

        if not finished:
            trace.voluntary_finish = False
            if aborted_on_llm_failures:
                trace.final_answer = "(no answer produced)"
                trace.sufficiency = {"met": False, "confidence": 0.0,
                                     "justification": trace.stopped_reason}
            else:
                trace.stopped_reason = f"max_steps ({self.cfg.max_steps}) reached"
                forced = self._force_finish(messages, trace)
                trace.final_answer = forced.get("answer", "(no answer produced)")
                trace.sufficiency = forced.get("sufficiency", {
                    "met": False, "confidence": 0.0,
                    "justification": "Stopped at step budget before the criterion was met."})
        trace.sources = sources
        trace.finished_at = now_iso()
        trace.elapsed_sec = time.time() - t0
        return trace

    def _force_finish(self, messages, trace):
        msgs = messages + [{"role": "user", "content":
            "You have reached the step budget. Based ONLY on observations so far, output a finish JSON now: "
            '{"answer": "...", "sufficiency": {"met": false, "confidence": 0.0-1.0, "justification": "..."}}'}]
        try:
            raw = self.llm.chat(msgs, force_json=self.cfg.force_json)
        except LLMError as e:
            return {"answer": "(no answer produced)",
                    "sufficiency": {"met": False, "confidence": 0.0,
                                    "justification": f"forced finish; LLM call failed: {e}"}}
        try:
            data = extract_json(raw)
            suff = data.get("sufficiency", {}) or {}
            answer = data.get("answer", "")
        except Exception:
            suff = {"met": False, "confidence": 0.0,
                    "justification": "forced finish; unparseable output"}
            answer = (raw or "").strip()[:500]
        if not self._has_grounded(trace):
            suff = {"met": False, "confidence": 0.0,
                    "justification": "Overridden: no Wikipedia section was ever read during "
                                     "this run, so the claimed sufficiency is not trusted."}
        else:
            suff = self._apply_relevance_gate(trace, answer, suff)
        return {"answer": answer, "sufficiency": suff}