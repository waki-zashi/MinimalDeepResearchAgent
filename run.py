import argparse
import json
import os
import re

from agent import DeepResearchAgent, Task
from config import Config, load_dotenv
from llm import LLM
from scoring import (build_summary, explicit_abstention, is_redirect, judge_verdict,
                     score, strict_score)
from trace import now_iso
from wikipedia_tools import WikipediaClient


def slugify(s, maxlen=60):
    s = re.sub(r"[^\w\- ]", "", s, flags=re.UNICODE).strip().replace(" ", "_")
    return s[:maxlen] or "task"


def load_questions(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Task(question=item["question"],
                 stop_criterion=item.get("stop_criterion"),
                 language=item.get("language", "en"),
                 gold=item.get("gold"),
                 expect_abstention=item.get("expect_abstention", False))
            for item in data]


def main():
    load_dotenv()
    p = argparse.ArgumentParser(description="Minimal Deep Research agent over Wikipedia")
    p.add_argument("--backend", choices=["groq", "gemini", "gigachat"], default="groq")
    p.add_argument("--groq-model", default=None)
    p.add_argument("--gemini-model", default=None)
    p.add_argument("--gigachat-model", default=None)
    p.add_argument("--language", default="en")
    p.add_argument("--max-steps", type=int, default=12)
    p.add_argument("--temperature", type=float, default=0.2)
    p.add_argument("--question", default=None)
    p.add_argument("--stop-criterion", default=None)
    p.add_argument("--batch", default=None)
    p.add_argument("--reports-dir", default="reports")
    p.add_argument("--relevance-gate", action="store_true")
    p.add_argument("--repeats", type=int, default=1)
    args = p.parse_args()

    cfg = Config(backend=args.backend, language=args.language,
                 max_steps=args.max_steps, temperature=args.temperature,
                 reports_dir=args.reports_dir, relevance_gate=args.relevance_gate)
    if args.groq_model:
        cfg.groq_model = args.groq_model
    if args.gemini_model:
        cfg.gemini_model = args.gemini_model
    if args.gigachat_model:
        cfg.gigachat_model = args.gigachat_model

    os.makedirs(cfg.reports_dir, exist_ok=True)
    agent = DeepResearchAgent(LLM(cfg),
                              WikipediaClient(language=cfg.language,
                                              timeout=cfg.request_timeout),
                              cfg)

    if args.batch:
        tasks = load_questions(args.batch)
    elif args.question:
        tasks = [Task(question=args.question, stop_criterion=args.stop_criterion,
                      language=args.language)]
    else:
        print("Provide --question or --batch")
        return

    repeats = max(1, args.repeats)
    rows = []
    resolved_model = ""
    json_mode = "n/a"
    total_tokens = 0
    for i, task in enumerate(tasks, 1):
        for r in range(1, repeats + 1):
            tag = f" (run {r}/{repeats})" if repeats > 1 else ""
            print(f"[{i}/{len(tasks)}]{tag} [{task.language}] {task.question}")
            trace = agent.run(task)
            trace.repeat = r
            resolved_model = trace.resolved_model or resolved_model
            json_mode = trace.json_mode or json_mode
            total_tokens += trace.token_usage.get("total_tokens", 0)
            suffix = f"_r{r}" if repeats > 1 else ""
            base = f"{i:02d}_{task.language}_{slugify(task.question)}{suffix}"
            with open(os.path.join(cfg.reports_dir, base + ".md"), "w", encoding="utf-8") as f:
                f.write(trace.to_markdown())
            with open(os.path.join(cfg.reports_dir, base + ".json"), "w", encoding="utf-8") as f:
                f.write(trace.to_json())
            met = trace.sufficiency.get("met")
            grounded = agent.has_grounded(trace)
            tool_errors = sum(1 for s in trace.steps
                              if (s.observation or "").startswith("Tool error"))
            rows.append({"i": i, "repeat": r, "question": task.question,
                         "language": task.language, "steps": len(trace.steps),
                         "sources": len(trace.sources),
                         "grounded": grounded, "tool_errors": tool_errors,
                         "met": met, "voluntary": trace.voluntary_finish,
                         "relevance_checked": trace.relevance_checked,
                         "judge": judge_verdict(trace.relevance, trace.relevance_checked,
                                                (met is not None and
                                                 trace.sufficiency.get("justification")) or ""),
                         "rejections": trace.grounding_rejections,
                         "tokens": trace.token_usage.get("total_tokens", 0),
                         "answer": trace.final_answer,
                         "explicit": explicit_abstention(trace.final_answer),
                         "match": score(met, trace.voluntary_finish, trace.final_answer,
                                        task.gold, task.expect_abstention,
                                        grounded, tool_errors),
                         "strict": strict_score(met, trace.voluntary_finish,
                                                trace.final_answer, task.gold,
                                                task.expect_abstention, grounded,
                                                tool_errors)})

    redirect = (" **(server-side redirect detected)**"
                if is_redirect(cfg.model, resolved_model) else "")
    header = [f"Backend: `{cfg.backend}`",
              f"Requested model: `{cfg.model}`",
              f"Model that actually answered: `{resolved_model or '(not reported)'}`{redirect}",
              f"JSON mode: {json_mode}",
              f"max_steps: {cfg.max_steps} — temperature: {cfg.temperature} — "
              f"relevance gate: {'ON' if cfg.relevance_gate else 'OFF'} — repeats: {repeats}",
              f"Total tokens across the batch: {total_tokens}",
              f"Generated: {now_iso()}"]
    with open(os.path.join(cfg.reports_dir, "summary.md"), "w", encoding="utf-8") as f:
        f.write(build_summary(header, rows, repeats))
    print(f"Done. Reports written to ./{cfg.reports_dir}/ "
          f"({len(rows)} runs, {total_tokens} tokens)")


if __name__ == "__main__":
    main()
