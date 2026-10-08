import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from audit_self_report import ABSENCE, CONCESSION, INFERENCE, self_report

REAL_CONTRADICTORY = [
    "Хотя прямой текстовой ссылки на руководство Борна не найдено, многочисленные упоминания "
    "его имени в контексте совместной работы указывают на его ключевую роль.",
    "Хотя явное указание национальности отсутствует, можно сделать вывод на основе места "
    "рождения и образования.",
    "Хотя явной информации о гражданстве нет, можно сделать вывод на основе места рождения.",
    "We have sufficient evidence pointing towards Arnold Sommerfeld being Heisenberg's "
    "doctoral advisor, though no single definitive statement exists.",
]

REAL_CLEAN = [
    "Explicitly stated in the lead section of the Wikipedia article.",
    "Информация получена непосредственно из соответствующего раздела статьи.",
    "Both the creator's name and the year of the first public release were explicitly stated "
    "in the 'History' section.",
    "Имеется достаточно информации для ответа на вопрос.",
]


def test_absence_pattern_fires_on_every_real_contradictory_self_report():
    for text in REAL_CONTRADICTORY:
        assert ABSENCE.search(text), text[:50]


def test_absence_pattern_stays_silent_on_real_clean_self_reports():
    for text in REAL_CLEAN:
        assert not ABSENCE.search(text), text[:50]


def test_concession_marker_separates_the_hedged_admissions():
    assert CONCESSION.search(REAL_CONTRADICTORY[0])
    assert not CONCESSION.search(REAL_CLEAN[0])


def test_inference_marker_fires_on_the_answers_that_announce_their_own_leap():
    assert INFERENCE.search("Эдсгер Дейкстра родился в Роттердаме, следовательно, он голландец.")
    assert INFERENCE.search("Дейкстра родился в Нидерландах, что позволяет предположить…")
    assert not INFERENCE.search("Edsger W. Dijkstra was Dutch.")
    assert not INFERENCE.search("Алан Тьюринг родился в Лондоне.")


def test_self_report_joins_the_justification_and_the_finish_note():
    trace = {"sufficiency": {"justification": "J"},
             "steps": [{"action": "read_section", "sufficiency_note": "ignored"},
                       {"action": "finish", "sufficiency_note": "N"}]}
    assert self_report(trace) == "J || N"


def test_the_audit_is_not_wired_into_the_agents_decision_path():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for name in ("agent.py", "run.py", "scoring.py", "relevance.py", "llm.py", "trace.py"):
        with open(os.path.join(here, name), encoding="utf-8") as f:
            assert "audit_self_report" not in f.read(), name
