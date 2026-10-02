import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import DeepResearchAgent, Task, extract_json
from config import Config


class ScriptedLLM:
    def __init__(self, scripted):
        self.scripted = list(scripted)
        self.calls = 0

    def chat(self, messages, temperature=None, max_tokens=None, force_json=False):
        out = self.scripted[self.calls] if self.calls < len(self.scripted) else self.scripted[-1]
        self.calls += 1
        return out


class BudgetLLM:
    def chat(self, messages, temperature=None, max_tokens=None, force_json=False):
        last = messages[-1]["content"] if messages else ""
        head = messages[0]["content"].lower() if messages else ""
        if "step budget" in last:
            return ('{"answer":"partial","sufficiency":'
                    '{"met":false,"confidence":0.2,"justification":"budget"}}')
        if "planning module" in head:
            return '{"sub_questions":[],"stop_criterion":"impossible","plan":"loop"}'
        return ('{"thought":"loop","sufficiency_note":"never done",'
                '"action":"search","action_input":{"query":"x"}}')


class FakeWiki:
    def search(self, query, limit=5, lang=None):
        return [{"title": "Alan Turing", "snippet": "mathematician"}]

    def get_sections(self, title, lang=None):
        return {"title": title, "sections": [
            {"index": "0", "level": "1", "line": "Lead"},
            {"index": "1", "level": "2", "line": "Education"}]}

    def read_section(self, title, section="0", lang=None, char_limit=None):
        resolved = "Alan Turing" if title == "Alan M. Turing" else title
        return {"title": resolved, "requested_title": title,
                "redirected": resolved != title, "section": str(section),
                "text": "Turing studied at King's College, Cambridge.",
                "truncated": False}


def test_extract_json_fenced():
    assert extract_json('```json\n{"a": 1}\n```')["a"] == 1


def test_extract_json_with_prose():
    assert extract_json('Sure! {"action": "finish"} done')["action"] == "finish"


def test_extract_json_repairs_trailing_comma():
    assert extract_json('{"thought": "ok", "action": "finish",}')["action"] == "finish"


def test_extract_json_repairs_missing_comma_between_fields():
    t = '{"thought": "ok"\n"action": "finish"}'
    assert extract_json(t)["action"] == "finish"


def test_agent_finishes_and_records_provenance():
    scripted = [
        '{"sub_questions":["Where did Turing study?"],'
        '"stop_criterion":"University confirmed by a read section","plan":"Find, read education."}',
        '{"thought":"search","sufficiency_note":"nothing yet","action":"search",'
        '"action_input":{"query":"Alan Turing"}}',
        '{"thought":"list sections","sufficiency_note":"need education","action":"get_sections",'
        '"action_input":{"title":"Alan Turing"}}',
        '{"thought":"read education","sufficiency_note":"reading","action":"read_section",'
        '"action_input":{"title":"Alan Turing","section":"1"}}',
        '{"thought":"done","sufficiency_note":"met","action":"finish",'
        '"action_input":{"answer":"King\'s College, Cambridge",'
        '"sufficiency":{"met":true,"confidence":0.9,"justification":"section confirms"}}}',
    ]
    cfg = Config(backend="groq")
    agent = DeepResearchAgent(ScriptedLLM(scripted), FakeWiki(), cfg)
    trace = agent.run(Task("Where did Alan Turing study?", language="en"))
    assert "King's College" in trace.final_answer
    assert trace.sufficiency.get("met") is True
    assert len(trace.sources) == 1
    assert trace.sources[0]["title"] == "Alan Turing"
    assert trace.stopped_reason == "agent called finish"
    assert len(trace.steps) == 4


class FlakyJSONLLM:
    def __init__(self, bad_then_good):
        self.bad_then_good = list(bad_then_good)
        self.calls = 0

    def chat(self, messages, temperature=None, max_tokens=None, force_json=False):
        out = self.bad_then_good[self.calls] if self.calls < len(self.bad_then_good) \
            else self.bad_then_good[-1]
        self.calls += 1
        return out


def test_unparseable_output_retries_without_charging_step_budget():
    scripted = [
        '{"sub_questions":[],"stop_criterion":"x","plan":"y"}',
        'not json at all',
        'still not json',
        '{"thought":"done","sufficiency_note":"n/a","action":"search",'
        '"action_input":{"query":"Alan Turing"}}',
    ]
    cfg = Config(backend="groq", max_steps=1)
    llm = FlakyJSONLLM(scripted)
    agent = DeepResearchAgent(llm, FakeWiki(), cfg)
    trace = agent.run(Task("q", language="en"))
    assert len(trace.steps) == 1
    assert trace.steps[0].action == "search"
    assert llm.calls == 5  # plan + 2 bad parses + 1 good + 1 forced-finish call


def test_user_provided_stop_criterion_is_kept():
    scripted = [
        '{"sub_questions":[],"stop_criterion":"AGENT VERSION","plan":"x"}',
        '{"thought":"done","sufficiency_note":"met","action":"finish",'
        '"action_input":{"answer":"ok","sufficiency":{"met":true}}}',
    ]
    cfg = Config(backend="groq")
    agent = DeepResearchAgent(ScriptedLLM(scripted), FakeWiki(), cfg)
    trace = agent.run(Task("q", stop_criterion="USER VERSION", language="en"))
    assert trace.stop_criterion == "USER VERSION"
    assert trace.stop_criterion_source == "provided by user"


def test_agent_hits_step_budget():
    cfg = Config(backend="groq", max_steps=3)
    agent = DeepResearchAgent(BudgetLLM(), FakeWiki(), cfg)
    trace = agent.run(Task("unanswerable", language="en"))
    assert "max_steps" in trace.stopped_reason
    assert trace.sufficiency.get("met") is False
    assert len(trace.steps) == 3


def test_markdown_render_smoke():
    scripted = [
        '{"sub_questions":[],"stop_criterion":"s","plan":"p"}',
        '{"thought":"t","sufficiency_note":"n","action":"finish",'
        '"action_input":{"answer":"A","sufficiency":{"met":true,"confidence":1.0,"justification":"j"}}}',
    ]
    cfg = Config(backend="groq")
    agent = DeepResearchAgent(ScriptedLLM(scripted), FakeWiki(), cfg)
    md = agent.run(Task("q", language="en")).to_markdown()
    assert "# Deep Research trace" in md
    assert "Stopping criterion" in md
    assert "Sources (provenance)" in md
