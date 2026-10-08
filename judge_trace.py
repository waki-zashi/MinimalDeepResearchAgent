import argparse
import json
import re
import sys

JUDGE_SYSTEM = (
    "You are a strict evidence verifier. You receive a QUESTION, a CLAIM and OBSERVATIONS "
    "(the text the agent actually read). Decide using ONLY the observations and ignore your own knowledge. "
    "Respond with exactly one JSON object: "
    '{"verdict": "supported" | "contradicted" | "insufficient", '
    '"evidence_quote": "<verbatim passage copied from OBSERVATIONS that directly states the claim, or empty string>", '
    '"missing": "<which fact is missing if insufficient>", '
    '"reasoning": "<2-3 sentences>"} '
    "'supported' requires a passage that explicitly states the specific relation the claim asserts. "
    "Related mentions, co-authorship, teaching contacts or plausible inference are NOT enough: use 'insufficient'. "
    "'contradicted' requires a passage that conflicts with the claim."
)


def load_trace(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def collect_observations(trace):
    seen = set()
    parts = []
    for s in trace.get("steps", []):
        if s.get("action") != "read_section":
            continue
        obs = s.get("observation", "")
        if obs.startswith("Tool error") or obs in seen:
            continue
        seen.add(obs)
        parts.append(obs)
    return "\n\n=====\n\n".join(parts)


def normalize(s):
    return re.sub(r"\s+", " ", s or "").strip().lower()


def extract_json(text):
    t = (text or "").strip()
    a = t.find("{")
    b = t.rfind("}")
    if a == -1 or b == -1 or b < a:
        raise ValueError(f"no JSON object in: {t[:200]}")
    return json.loads(t[a:b + 1])


def judge(llm, question, claim, observations):
    user = f"QUESTION:\n{question}\n\nCLAIM:\n{claim}\n\nOBSERVATIONS:\n{observations}"
    messages = [{"role": "system", "content": JUDGE_SYSTEM},
                {"role": "user", "content": user}]
    try:
        raw = llm.chat(messages, force_json=True)
    except TypeError:
        raw = llm.chat(messages)
    data = extract_json(raw)
    quote = data.get("evidence_quote", "") or ""
    quote_ok = bool(quote) and normalize(quote) in normalize(observations)
    if data.get("verdict") == "supported" and not quote_ok:
        data["verdict"] = "insufficient"
        data["downgraded"] = "evidence_quote is not a literal substring of the observations"
    data["quote_found_in_observations"] = quote_ok
    return data


def make_llm(backend):
    from config import Config, load_dotenv
    from llm import LLM
    load_dotenv()
    return LLM(Config(backend=backend))


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("trace")
    p.add_argument("--backend", default="gigachat")
    p.add_argument("--control", action="append", default=[])
    p.add_argument("--out", default=None)
    args = p.parse_args()

    trace = load_trace(args.trace)
    observations = collect_observations(trace)
    llm = make_llm(args.backend)

    claims = [("agent_answer", trace.get("final_answer", ""))]
    claims += [(f"control_{i + 1}", c) for i, c in enumerate(args.control)]

    results = {}
    for name, claim in claims:
        res = judge(llm, trace.get("question", ""), claim, observations)
        results[name] = {"claim": claim, **res}
        print(f"[{name}] {res['verdict']}  (quote found: {res['quote_found_in_observations']})")
        print(f"  claim:     {claim}")
        print(f"  quote:     {res.get('evidence_quote', '')}")
        print(f"  missing:   {res.get('missing', '')}")
        print(f"  reasoning: {res.get('reasoning', '')}")
        if res.get("downgraded"):
            print(f"  note:      {res['downgraded']}")
        print()

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()