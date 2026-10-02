import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import DeepResearchAgent, Task, extract_json
from config import Config
from relevance import judge_relevance

from test_agent_mock import FakeWiki


class ScriptedLLM:
    def __init__(self, scripted):
        self.scripted = list(scripted)
        self.calls = 0

    def chat(self, messages, temperature=None, max_tokens=None, force_json=False):
        out = self.scripted[self.calls] if self.calls < len(self.scripted) else self.scripted[-1]
        self.calls += 1
        return out


class JudgeOnlyLLM:
    """A fake chat_fn for judge_relevance() unit tests - ignores messages, returns scripted JSON."""
    def __init__(self, response):
        self.response = response
        self.calls = 0

    def __call__(self, messages, force_json=False):
        self.calls += 1
        return self.response


def test_judge_relevance_rejects_unsupported_answer():
    judge = JudgeOnlyLLM('{"supported": false, "reasoning": "passages are about a different person"}')
    supported, reasoning = judge_relevance(judge, extract_json, "q", "answer", ["some passage"])
    assert supported is False
    assert "different person" in reasoning
    assert judge.calls == 1


def test_judge_relevance_accepts_supported_answer():
    judge = JudgeOnlyLLM('{"supported": true, "reasoning": "the passage states it directly"}')
    supported, reasoning = judge_relevance(judge, extract_json, "q", "answer", ["some passage"])
    assert supported is True


def test_judge_relevance_rejects_with_no_observations():
    judge = JudgeOnlyLLM('{"supported": true, "reasoning": "n/a"}')
    supported, reasoning = judge_relevance(judge, extract_json, "q", "answer", [])
    assert supported is False
    assert judge.calls == 0  # never even calls the judge - nothing to check against


def test_judge_relevance_treats_judge_call_failure_as_unsupported():
    def broken_chat(messages, force_json=False):
        raise RuntimeError("API down")
    supported, reasoning = judge_relevance(broken_chat, extract_json, "q", "answer", ["x"])
    assert supported is False
    assert "API down" in reasoning


def test_judge_relevance_treats_unparseable_judge_output_as_unsupported():
    judge = JudgeOnlyLLM("not json at all")
    supported, reasoning = judge_relevance(judge, extract_json, "q", "answer", ["x"])
    assert supported is False


def test_relevance_gate_overrides_cormen_style_case():
    """Reproduces the real failure from the GigaChat batch (question 1): the agent read
    a passage about Thomas H. Cormen (co-author of a textbook) and answered with HIS
    birth city, while the question was about a completely different person (the 'founder
    of the theory of algorithms... famous test named after him', i.e. Alan Turing).
    grounded=True (a real read_section happened) and the agent's own sufficiency said
    met=True/confidence=1.0 - exactly what slipped through before this gate existed."""
    scripted = [
        '{"sub_questions":[],"stop_criterion":"birth city confirmed by a read section","plan":"x"}',
        '{"thought":"search","sufficiency_note":"n/a","action":"search","action_input":{"query":"founder of the theory of algorithms"}}',
        '{"thought":"read","sufficiency_note":"n/a","action":"read_section","action_input":{"title":"Thomas H. Cormen","section":"1"}}',
        '{"thought":"done","sufficiency_note":"met","action":"finish","action_input":'
        '{"answer":"Thomas H. Cormen was born in New York City.",'
        '"sufficiency":{"met":true,"confidence":1.0,"justification":"confirmed by his bio"}}}',
        # the next scripted response is consumed by the relevance judge call:
        '{"supported": false, "reasoning": "the passage is about Thomas H. Cormen, not the '
        'person the question asks about (the founder of the theory of algorithms with a '
        'famous test named after him)"}',
    ]
    cfg = Config(backend="groq", relevance_gate=True)
    agent = DeepResearchAgent(ScriptedLLM(scripted), FakeWiki(), cfg)
    trace = agent.run(Task(
        "In which city was the person who is considered the founder of the theory of "
        "algorithms and who has a famous test named after him born?", language="en"))
    assert "Cormen" in trace.final_answer
    assert trace.relevance_checked is True
    assert trace.sufficiency.get("met") is False
    assert "Overridden by relevance gate" in trace.sufficiency.get("justification", "")


def test_relevance_gate_overrides_dijkstra_style_false_syllogism():
    """Reproduces the second real failure (question 2): the agent read a passage that only
    mentions Dijkstra working/shopping in Amsterdam and Rotterdam - no nationality word at
    all - then answered 'Dutch' via the unstated inference 'worked in Amsterdam => Dutch'.
    The answer happens to match gold, but the chain of reasoning is not supported by the
    text, which is exactly what this gate is meant to catch."""
    scripted = [
        '{"sub_questions":[],"stop_criterion":"nationality confirmed by a read section","plan":"x"}',
        '{"thought":"search","sufficiency_note":"n/a","action":"search","action_input":{"query":"Dijkstra algorithm"}}',
        '{"thought":"read","sufficiency_note":"n/a","action":"read_section","action_input":{"title":"Dijkstra'"'"'s algorithm","section":"1"}}',
        '{"thought":"done","sufficiency_note":"met","action":"finish","action_input":'
        '{"answer":"Dutch",'
        '"sufficiency":{"met":true,"confidence":1.0,"justification":"he worked in Amsterdam, commonly Dutch"}}}',
        '{"supported": false, "reasoning": "the passage mentions Amsterdam and Rotterdam but '
        'never states a nationality; Dutch is inferred, not read"}',
    ]
    cfg = Config(backend="groq", relevance_gate=True)
    agent = DeepResearchAgent(ScriptedLLM(scripted), FakeWiki(), cfg)
    trace = agent.run(Task(
        "What is the nationality of the mathematician after whom the programming construct "
        "'Dijkstra's algorithm' is named?", language="en"))
    assert trace.final_answer == "Dutch"
    assert trace.sufficiency.get("met") is False
    assert "Overridden by relevance gate" in trace.sufficiency.get("justification", "")


def test_relevance_gate_leaves_genuinely_supported_answer_alone():
    scripted = [
        '{"sub_questions":[],"stop_criterion":"x","plan":"y"}',
        '{"thought":"read","sufficiency_note":"n/a","action":"read_section","action_input":{"title":"Alan Turing","section":"0"}}',
        '{"thought":"done","sufficiency_note":"met","action":"finish","action_input":'
        '{"answer":"London","sufficiency":{"met":true,"confidence":0.95,"justification":"stated directly"}}}',
        '{"supported": true, "reasoning": "the passage states the birth city directly"}',
    ]
    cfg = Config(backend="groq", relevance_gate=True)
    agent = DeepResearchAgent(ScriptedLLM(scripted), FakeWiki(), cfg)
    trace = agent.run(Task("Where was Alan Turing born?", language="en"))
    assert trace.sufficiency.get("met") is True
    assert trace.relevance_checked is True


def test_relevance_gate_off_by_default_does_not_call_judge():
    scripted = [
        '{"sub_questions":[],"stop_criterion":"x","plan":"y"}',
        '{"thought":"read","sufficiency_note":"n/a","action":"read_section","action_input":{"title":"Alan Turing","section":"0"}}',
        '{"thought":"done","sufficiency_note":"met","action":"finish","action_input":'
        '{"answer":"London","sufficiency":{"met":true,"confidence":0.95,"justification":"stated directly"}}}',
    ]
    cfg = Config(backend="groq")  # relevance_gate defaults to False
    llm = ScriptedLLM(scripted)
    agent = DeepResearchAgent(llm, FakeWiki(), cfg)
    trace = agent.run(Task("Where was Alan Turing born?", language="en"))
    assert trace.sufficiency.get("met") is True
    assert trace.relevance_checked is False
    assert llm.calls == len(scripted)  # no extra judge call consumed
