import re

ABSTENTION_MARKERS = [
    "not enough", "insufficient", "not sufficient", "cannot be determined",
    "can not be determined", "could not be determined", "unable to determine",
    "no evidence", "no explicit", "not explicitly", "not stated", "does not state",
    "do not state", "no concrete", "no mention", "not mentioned", "no information",
    "not available", "not found", "unknown",
    "недостаточно", "не удалось", "не указан", "не указано", "не указаны",
    "нет сведений", "нет данных", "нет информации", "невозможно определить",
    "не определено", "не содержат", "не содержится", "отсутству", "неизвестно",
    "невозможно", "не могу", "нельзя установить", "нет точных",
    "достаточной информации", "доступной информации", "достаточных данных",
    "не найдено", "не упомина",
]


def normalize(s):
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def match_gold(answer, gold):
    if not gold:
        return None
    a = normalize(answer)
    if isinstance(gold, list):
        return any(normalize(g) in a for g in gold)
    return normalize(gold) in a


def base_model_id(name):
    return (name or "").split(":", 1)[0].strip()


def is_redirect(requested, resolved):
    if not resolved:
        return False
    return base_model_id(requested) != base_model_id(resolved)


def is_grounding_observation(action, observation, min_chars):
    if action != "read_section":
        return False
    if not observation or observation.startswith("Tool error"):
        return False
    _, _, body = observation.partition("\n")
    body = body.replace("[truncated]", "").strip()
    if body in ("", "(empty section)"):
        return False
    return len(body) >= min_chars


def voluntary_abstention(met, voluntary_finish, grounded=True, tool_errors=0):
    """A credited abstention is one the agent reached from evidence: it finished on its own,
    had read at least one usable passage, and was not driven to give up by tool failures.
    An abstention produced after failed tool calls is correct in outcome but not in cause,
    so it is not counted as a success."""
    return (met is False and bool(voluntary_finish) and bool(grounded)
            and not tool_errors)


def explicit_abstention(answer):
    a = normalize(answer)
    if not a or a == "(no answer produced)":
        return True
    return any(m in a for m in ABSTENTION_MARKERS)


def score(met, voluntary_finish, answer, gold, expect_abstention,
          grounded=True, tool_errors=0):
    if expect_abstention:
        return voluntary_abstention(met, voluntary_finish, grounded, tool_errors)
    return match_gold(answer, gold)


def strict_score(met, voluntary_finish, answer, gold, expect_abstention,
                 grounded=True, tool_errors=0):
    """Same as score(), but a gold match only counts when the agent itself claimed the
    stopping criterion was met. A correct string produced under met:false is a lucky
    substring, not an answer the agent stood behind."""
    if expect_abstention:
        return None
    base = score(met, voluntary_finish, answer, gold, expect_abstention,
                 grounded, tool_errors)
    if base is None:
        return None
    return bool(base) and met is True


def build_summary(header, rows, repeats):
    lines = ["# Batch summary\n"] + [f"- {h}  " for h in header] + ["",
             "| # | Run | Lang | Question | Steps | Sources | Grounded | Stop met | "
             "Voluntary | Judge | Tool err | Gold/abstention | Gold & met | "
             "Verbal abst. | Tokens | Answer |",
             "|---|-----|------|----------|-------|---------|----------|----------|"
             "-----------|-------|----------|-----------------|------------|"
             "--------------|--------|--------|"]
    for s in rows:
        ans = (s["answer"] or "").replace("\n", " ").replace("|", "\\|")
        ans = ans[:80] + "…" if len(ans) > 80 else ans
        q = s["question"].replace("|", "\\|")
        q = q[:60] + "…" if len(q) > 60 else q
        match = "" if s["match"] is None else ("YES" if s["match"] else "NO")
        strict = ("" if s.get("strict") is None
                  else ("YES" if s.get("strict") else "NO"))
        verbal = "yes" if s["explicit"] else ""
        lines.append(f"| {s['i']} | {s['repeat']} | {s['language']} | {q} | {s['steps']} | "
                     f"{s['sources']} | {s['grounded']} | {s['met']} | "
                     f"{s['voluntary']} | {s.get('judge', '—')} | "
                     f"{s.get('tool_errors', 0)} | {match} | {strict} | "
                     f"{verbal} | {s['tokens']} | {ans} |")
    if repeats > 1:
        from collections import defaultdict
        agg = defaultdict(list)
        for s in rows:
            agg[(s["i"], s["language"])].append(s)
        lines.append("\n## Reproducibility across repeats\n")
        lines.append("| # | Lang | Stop met | Gold/abstention | Gold & met | "
                     "Tool err | Question |")
        lines.append("|---|------|----------|-----------------|------------|"
                     "----------|----------|")
        for (i, lang), group in sorted(agg.items()):
            k = len(group)
            met = sum(1 for s in group if s["met"] is True)
            hit = sum(1 for s in group if s["match"] is True)
            strict = sum(1 for s in group if s.get("strict") is True)
            terr = sum(1 for s in group if s.get("tool_errors", 0))
            q = group[0]["question"].replace("|", "\\|")
            q = q[:60] + "…" if len(q) > 60 else q
            scored = "n/a" if group[0]["match"] is None else f"{hit}/{k}"
            strict_cell = ("n/a" if group[0].get("strict") is None else f"{strict}/{k}")
            lines.append(f"| {i} | {lang} | {met}/{k} | {scored} | {strict_cell} | "
                         f"{terr}/{k} | {q} |")
    return "\n".join(lines)


def judge_verdict(relevance, relevance_checked, justification):
    """How to label the relevance judge in a summary row, including for traces written
    before the verdict itself was recorded."""
    if relevance:
        return "supported" if relevance.get("supported") else "overridden"
    if not relevance_checked:
        return "—"
    if "overridden by relevance gate" in (justification or "").lower():
        return "overridden"
    return "supported (not recorded)"
