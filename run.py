import argparse
import json
import os
import re

from agent import DeepResearchAgent, Task
from config import Config, load_dotenv
from llm import LLM
from trace import now_iso
from wikipedia_tools import WikipediaClient


def slugify(s, maxlen=60):
    s = re.sub(r"[^\w\- ]", "", s, flags=re.UNICODE).strip().replace(" ", "_")
    return s[:maxlen] or "task"


def normalize(s):
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def match_gold(answer, gold):
    if not gold:
        return None
    a = normalize(answer)
    if isinstance(gold, list):
        return any(normalize(g) in a for g in gold)
    return normalize(gold) in a


def load_questions(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Task(question=item["question"],
                 stop_criterion=item.get("stop_criterion"),
                 language=item.get("language", "en"),
                 gold=item.get("gold")) for item in data]


def main():
    load_dotenv()
    p = argparse.ArgumentParser(description="Minimal Deep Research agent over Wikipedia")
    p.add_argument("--backend", choices=["groq", "gemini", "gigachat"], default="groq")
    p.add_argument("--groq-model", default=None)
    p.add_argument("--gemini-model", default=None)
    p.add_argument("--gigachat-model", default=None)
    p.add_argument("--language", default="en")
    p.add_argument("--max-steps", type=int, default=8)
    p.add_argument("--temperature", type=float, default=0.2)
    p.add_argument("--question", default=None)
    p.add_argument("--stop-criterion", default=None)
    p.add_argument("--batch", default=None)
    p.add_argument("--reports-dir", default="reports")
    p.add_argument("--relevance-gate", action="store_true")
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

    summary = []
    for i, task in enumerate(tasks, 1):
        print(f"[{i}/{len(tasks)}] {task.question}")
        trace = agent.run(task)
        base = f"{i:02d}_{slugify(task.question)}"
        with open(os.path.join(cfg.reports_dir, base + ".md"), "w", encoding="utf-8") as f:
            f.write(trace.to_markdown())
        with open(os.path.join(cfg.reports_dir, base + ".json"), "w", encoding="utf-8") as f:
            f.write(trace.to_json())
        grounded = any(s.action in {"search", "get_sections", "read_section"}
                      and not s.observation.startswith("Tool error")
                      for s in trace.steps)
        summary.append({"i": i, "question": task.question, "steps": len(trace.steps),
                        "sources": len(trace.sources), "grounded": grounded,
                        "met": trace.sufficiency.get("met"),
                        "answer": trace.final_answer,
                        "match": match_gold(trace.final_answer, task.gold)})

    lines = ["# Batch summary\n",
             f"Backend / model: `{cfg.backend}` / `{cfg.model}` — generated {now_iso()}\n",
             "| # | Question | Steps | Sources | Grounded | Stop met | Gold match | Answer |",
             "|---|----------|-------|---------|----------|----------|-----------|--------|"]
    for s in summary:
        ans = (s["answer"] or "").replace("\n", " ").replace("|", "\\|")
        ans = ans[:80] + "…" if len(ans) > 80 else ans
        q = s["question"].replace("|", "\\|")
        q = q[:60] + "…" if len(q) > 60 else q
        match = "" if s["match"] is None else ("YES" if s["match"] else "NO")
        lines.append(f"| {s['i']} | {q} | {s['steps']} | {s['sources']} | {s['grounded']} | {s['met']} | {match} | {ans} |")
    with open(os.path.join(cfg.reports_dir, "summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Done. Reports written to ./{cfg.reports_dir}/")


if __name__ == "__main__":
    main()