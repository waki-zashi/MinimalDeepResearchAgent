RELEVANCE_JUDGE_SYSTEM = """You are a strict fact-checking judge for a Wikipedia research agent.
You are given a question, the agent's proposed final answer, and the exact passages the agent
actually read from Wikipedia during its investigation. Your only job is to decide whether the
proposed answer follows DIRECTLY from those passages, with no outside knowledge and no unstated
inferential leap.

Reject (supported: false) if:
- the answer is about a different entity than the one the question and passages are about
  (e.g. the question asks about person X, the passages are about an unrelated person Y, and the
  answer is derived from Y instead of X);
- the answer relies on an inference the passages do not state (e.g. inferring nationality from a
  city of residence, inferring a date from an unrelated event, "commonly known" facts not present
  in the text);
- the passages do not mention the key fact the answer asserts, even if the general topic overlaps.

Accept (supported: true) only if the specific fact in the answer is stated or very directly
implied by the passages themselves.

Respond with EXACTLY ONE JSON object and nothing else:
{"supported": true|false, "reasoning": "<one sentence, citing what the passages do or don't say>"}
"""


def relevance_judge_prompt(question, answer, observations):
    if not observations:
        obs_text = "(no passages were read)"
    else:
        obs_text = "\n\n".join(f"[Observation {i + 1}]\n{o}"
                               for i, o in enumerate(observations))
    return (f"Question: {question}\n\n"
            f"Proposed answer: {answer}\n\n"
            f"Passages actually read from Wikipedia during this run:\n{obs_text}\n\n"
            "Judge whether the proposed answer is directly supported by these passages. "
            "Output the JSON object now.")


def judge_relevance(chat_fn, extract_json_fn, question, answer, observations):
    """Ask a judge (any chat_fn(messages, force_json=True) -> str) whether `answer`
    is directly supported by `observations`. Returns (supported: bool, reasoning: str).
    Never raises - any failure (bad judge output, judge call failure) is treated as
    "not supported", since an unverifiable answer should not be trusted silently."""
    if not observations:
        return False, "no observations were read, so the answer cannot be checked"
    msgs = [{"role": "system", "content": RELEVANCE_JUDGE_SYSTEM},
            {"role": "user", "content": relevance_judge_prompt(question, answer, observations)}]
    try:
        raw = chat_fn(msgs, force_json=True)
    except Exception as e:
        return False, f"relevance judge call failed: {e}"
    try:
        data = extract_json_fn(raw)
    except Exception as e:
        return False, f"relevance judge produced unparseable output: {e}"
    return bool(data.get("supported")), str(data.get("reasoning", "")) or "(no reasoning given)"
