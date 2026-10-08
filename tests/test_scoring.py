import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scoring import (explicit_abstention, is_grounding_observation, is_redirect,
                     match_gold, score, voluntary_abstention)


def test_build_version_suffix_is_not_a_redirect():
    assert is_redirect("GigaChat-2-Max", "GigaChat-2-Max:2.0.28.2") is False


def test_different_model_family_is_a_redirect():
    assert is_redirect("GigaChat", "GigaChat-2-Lite:2.0.28.2") is True
    assert is_redirect("GigaChat-2-Max", "GigaChat-2-Lite") is True


def test_missing_resolved_model_is_not_reported_as_redirect():
    assert is_redirect("GigaChat-2-Max", "") is False


def test_abstention_is_scored_structurally_not_by_keywords():
    answer = ("Based on the reviewed sections of the 'History of Python' article, there is "
              "no explicit statement regarding the number of lines of source code.")
    assert score(False, True, answer, None, True) is True
    assert voluntary_abstention(False, True) is True


def test_russian_abstention_without_english_keywords_is_scored():
    answer = ("Точное число строк исходного кода первого публичного выпуска интерпретатора "
              "Python неизвестно из доступных источников.")
    assert score(False, True, answer, None, True) is True
    assert explicit_abstention(answer) is True


def test_claiming_the_criterion_was_met_fails_an_abstention_task():
    assert score(True, True, "It contained 12000 lines.", None, True) is False


def test_budget_exhaustion_is_not_credited_as_abstention():
    assert score(False, False, "(no answer produced)", None, True) is False


def test_gold_matching_accepts_either_transliteration():
    gold = ["Łukasiewicz", "Lukasiewicz", "Лукасевич", "Лукашевич"]
    assert match_gold("Ян Лукашевич работал в Варшавском университете", gold) is True
    assert match_gold("Jan Łukasiewicz worked at Lemberg", gold) is True
    assert match_gold("Alfred Tarski", gold) is False


def test_grounding_predicate_matches_the_agents_rule():
    assert is_grounding_observation("read_section", "Alan Turing — section 1:\n(empty section)", 32) is False
    assert is_grounding_observation("read_section", "Alan Turing — section 1:\nShort.", 32) is False
    assert is_grounding_observation("search", "- Alan Turing: mathematician and logician of note", 32) is False
    assert is_grounding_observation(
        "read_section", "Alan Turing — section 1:\nTuring studied at King's College, Cambridge.", 32) is True


def test_judge_verdict_labels():
    from scoring import judge_verdict
    assert judge_verdict({"supported": True}, True, "") == "supported"
    assert judge_verdict({"supported": False}, True, "") == "overridden"
    assert judge_verdict(None, False, "") == "—"
    assert judge_verdict(None, True, "Overridden by relevance gate: nope") == "overridden"
    assert judge_verdict(None, True, "section confirms") == "supported (not recorded)"


def test_markers_cover_the_abstention_that_slipped_through():
    from scoring import explicit_abstention
    assert explicit_abstention("На данный момент невозможно точно указать число строк.") is True


def test_repeats_of_one_question_are_grouped_not_counted_separately():
    from scoring import build_summary
    rows = []
    for r in (1, 2, 3):
        rows.append({"i": 1, "repeat": r, "question": "Q", "language": "ru", "steps": 4,
                     "sources": 1, "grounded": True, "met": r != 2, "voluntary": True,
                     "judge": "supported", "tool_errors": 0, "tokens": 100,
                     "answer": "A", "explicit": False, "match": r != 3,
                     "strict": r == 1})
    out = build_summary(["h"], rows, 3)
    assert "| 1 | ru | 2/3 | 2/3 | 1/3 | 0/3 | Q |" in out


def test_gold_covers_the_granularity_each_language_article_uses():
    import json
    from scoring import match_gold
    tasks = json.load(open("questions.bilingual.json", encoding="utf-8"))
    gold = [t["gold"] for t in tasks if t["id"] == 1][0]
    assert match_gold("Вестминстер", gold) is True
    assert match_gold("Лондон", gold) is True
    assert match_gold("Maida Vale, London", gold) is True
    assert match_gold("Тамбов", gold) is False


def test_tool_failure_abstention_is_not_credited():
    from scoring import score, voluntary_abstention
    answer = "Due to ongoing technical difficulties preventing retrieval of essential sections…"
    assert score(False, True, answer, None, True, grounded=True, tool_errors=5) is False
    assert voluntary_abstention(False, True, grounded=True, tool_errors=0) is True
    assert voluntary_abstention(False, True, grounded=False, tool_errors=0) is False


def test_gold_hit_under_met_false_is_not_a_strict_hit():
    from scoring import score, strict_score
    ans = "Эдсгер Дейкстра родился в Нидерландах, что позволяет предположить, что он голландец."
    gold = ["Dutch", "Netherlands", "нидерланд", "голланд"]
    assert score(False, True, ans, gold, False) is True
    assert strict_score(False, True, ans, gold, False) is False
    assert strict_score(True, True, ans, gold, False) is True


def test_strict_score_is_none_for_abstention_rows():
    from scoring import strict_score
    assert strict_score(False, True, "no data", None, True) is None


def test_markers_cover_the_two_phrasings_that_were_missed():
    from scoring import explicit_abstention
    assert explicit_abstention("В статьях нет достаточной информации об этом.") is True
    assert explicit_abstention("Нет доступной информации о числе строк.") is True
