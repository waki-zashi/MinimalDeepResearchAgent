import argparse
import glob
import json
import os

from config import Config
from scoring import (build_summary, explicit_abstention, is_grounding_observation,
                     is_redirect, judge_verdict, score, strict_score)
from trace import now_iso


def load_batch(path):
    if not path:
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {item["question"]: (item.get("gold"), item.get("expect_abstention", False))
            for item in data}


def main():
    p = argparse.ArgumentParser(
        description="Rebuild summary.md from the saved JSON traces of a finished run, "
                    "without calling any API again.")
    p.add_argument("reports_dirs", nargs="+",
                   help="one or more report directories, scored as a single dataset "
                        "(use this to splice a re-run of individual questions into a batch)")
    p.add_argument("--drop-aborted", action="store_true",
                   help="exclude runs that were aborted by consecutive LLM/transport "
                        "failures; the count of excluded runs is reported")
    p.add_argument("--batch", default=None,
                   help="question set whose gold/expect_abstention fields override "
                        "the ones stored in the traces")
    p.add_argument("--min-grounding-chars", type=int, default=Config().min_grounding_chars)
    p.add_argument("--out", default=None)
    args = p.parse_args()

    overrides = load_batch(args.batch)
    task_index = {}
    unmatched = set()
    paths = []
    for d in args.reports_dirs:
        paths.extend(sorted(glob.glob(os.path.join(d, "*.json"))))
    aborted = 0
    seen = {}
    rows = []
    resolved_model = ""
    requested_model = ""
    backend = ""
    json_mode = "n/a"
    relevance_gate = False
    total_tokens = 0
    max_steps = 0
    temperature = None
    repeats = 1
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
        if "steps" not in d or "sufficiency" not in d:
            continue
        if args.drop_aborted and "aborted after" in (d.get("stopped_reason") or ""):
            aborted += 1
            continue
        dup = (d["question"], d.get("language", ""), d.get("repeat", 1))
        seen.setdefault(dup, []).append(os.path.basename(path))
        backend = d.get("backend", backend)
        requested_model = d.get("model", requested_model)
        resolved_model = d.get("resolved_model") or resolved_model
        json_mode = d.get("json_mode") or json_mode
        relevance_gate = relevance_gate or d.get("relevance_checked", False)
        tokens = (d.get("token_usage") or {}).get("total_tokens", 0)
        total_tokens += tokens
        max_steps = max(max_steps, len(d["steps"]))
        repeats = max(repeats, d.get("repeat", 1))
        if overrides and d["question"] not in overrides:
            unmatched.add(d["question"])
        gold, expect = overrides.get(d["question"],
                                     (d.get("gold"), d.get("expect_abstention", False)))
        met = d["sufficiency"].get("met")
        voluntary = d.get("voluntary_finish", False)
        grounded = any(is_grounding_observation(s.get("action", ""), s.get("observation", ""),
                                                args.min_grounding_chars)
                       for s in d["steps"])
        tool_errors = sum(1 for s in d["steps"]
                          if (s.get("observation") or "").startswith("Tool error"))
        key = (d["question"], d.get("language", ""))
        task_index.setdefault(key, len(task_index) + 1)
        rows.append({"i": task_index[key], "repeat": d.get("repeat", 1),
                     "question": d["question"], "language": d.get("language", ""),
                     "steps": len(d["steps"]), "sources": len(d.get("sources", [])),
                     "grounded": grounded, "met": met, "voluntary": voluntary,
                     "relevance_checked": d.get("relevance_checked", False),
                     "judge": judge_verdict(d.get("relevance"),
                                            d.get("relevance_checked", False),
                                            d["sufficiency"].get("justification", "")),
                     "rejections": d.get("grounding_rejections", 0),
                     "tokens": tokens, "answer": d.get("final_answer", ""),
                     "tool_errors": tool_errors,
                     "explicit": explicit_abstention(d.get("final_answer", "")),
                     "match": score(met, voluntary, d.get("final_answer", ""), gold, expect,
                                    grounded, tool_errors),
                     "strict": strict_score(met, voluntary, d.get("final_answer", ""),
                                            gold, expect, grounded, tool_errors)})

    dups = {k: v for k, v in seen.items() if len(v) > 1}
    if dups:
        print(f"WARNING: {len(dups)} question/language/repeat slot(s) appear more than once "
              f"- the dataset double-counts them:")
        for (q, lang, r), files in sorted(dups.items())[:10]:
            print(f"  - [{lang} r{r}] {q[:60]} <- {', '.join(files)}")
    redirect = (" **(server-side redirect detected)**"
                if is_redirect(requested_model, resolved_model) else "")
    header = [f"Backend: `{backend}`",
              f"Requested model: `{requested_model}`",
              f"Model that actually answered: `{resolved_model or '(not reported)'}`{redirect}",
              f"JSON mode: {json_mode}",
              f"Relevance gate: {'ON' if relevance_gate else 'OFF'} — "
              f"longest run: {max_steps} steps",
              f"Total tokens across the batch: {total_tokens}",
              f"Rescored from saved traces in "
              + ", ".join(f"`{d}`" for d in args.reports_dirs)
              + (f" (excluding {aborted} run(s) aborted by transport failures)"
                 if aborted else "")
              + (f" against `{args.batch}`" if args.batch else "")
              + f" — {now_iso()}"]
    out = args.out or os.path.join(args.reports_dirs[0], "summary.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(build_summary(header, rows, repeats))

    if unmatched:
        print(f"WARNING: {len(unmatched)} question(s) in these traces are not in "
              f"{args.batch}; they were scored against the gold stored in the trace, "
              f"which may be stale:")
        for q in sorted(unmatched):
            print(f"  - {q[:100]}")
    scored = [r for r in rows if r["match"] is not None]
    gold_rows = [r for r in scored if r["strict"] is not None]
    abst = [r for r in scored if r["strict"] is None]
    hits = sum(1 for r in scored if r["match"])
    print(f"Rescored {len(rows)} traces -> {out}")
    print(f"  gold/abstention (any):        {hits}/{len(scored)}")
    print(f"  gold hit while met:true:     "
          f"{sum(1 for r in gold_rows if r['strict'])}/{len(gold_rows)}")
    print(f"  credited abstentions:        "
          f"{sum(1 for r in abst if r['match'])}/{len(abst)}"
          f"  (excluded for tool failures: "
          f"{sum(1 for r in abst if r['tool_errors'] and not r['match'])})")
    print(f"  stop criterion met:          {sum(1 for r in rows if r['met'] is True)}/{len(rows)}")
    print(f"  grounded:                    {sum(1 for r in rows if r['grounded'])}/{len(rows)}")
    print(f"  runs with tool errors:       {sum(1 for r in rows if r['tool_errors'])}/{len(rows)}"
          f"  ({sum(r['tool_errors'] for r in rows)} errors total)")
    if aborted:
        print(f"  excluded as aborted:         {aborted} (transport/LLM failure, not an "
              f"agent decision - disclose this in the write-up)")


if __name__ == "__main__":
    main()
