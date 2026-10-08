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


class EmptySectionWiki(FakeWiki):
    def read_section(self, title, section="0", lang=None, char_limit=None):
        return {"title": title, "requested_title": title, "redirected": False,
                "section": str(section), "text": "", "truncated": False}


class TinySectionWiki(FakeWiki):
    def read_section(self, title, section="0", lang=None, char_limit=None):
        return {"title": title, "requested_title": title, "redirected": False,
                "section": str(section), "text": "See also.", "truncated": False}


def _read_then_finish_script():
    return [
        '{"sub_questions":[],"stop_criterion":"x","plan":"y"}',
        '{"thought":"read","sufficiency_note":"n/a","action":"read_section",'
        '"action_input":{"title":"Alan Turing","section":"1"}}',
        '{"thought":"done","sufficiency_note":"met","action":"finish","action_input":'
        '{"answer":"London","sufficiency":{"met":true,"confidence":1.0,"justification":"read it"}}}',
    ]


def test_empty_section_is_not_counted_as_grounding():
    cfg = Config(backend="groq", max_steps=3)
    agent = DeepResearchAgent(ScriptedLLM(_read_then_finish_script()), EmptySectionWiki(), cfg)
    trace = agent.run(Task("Where was Alan Turing born?", language="en"))
    assert agent.has_grounded(trace) is False
    assert trace.grounding_rejections == 1
    assert trace.sufficiency.get("met") is False
    assert "grounding gate" in trace.sufficiency.get("justification", "")
    assert trace.voluntary_finish is False


def test_near_empty_section_is_not_counted_as_grounding():
    cfg = Config(backend="groq", max_steps=3)
    agent = DeepResearchAgent(ScriptedLLM(_read_then_finish_script()), TinySectionWiki(), cfg)
    trace = agent.run(Task("Where was Alan Turing born?", language="en"))
    assert agent.has_grounded(trace) is False
    assert trace.sufficiency.get("met") is False


def test_real_section_body_still_counts_as_grounding():
    cfg = Config(backend="groq", max_steps=3)
    agent = DeepResearchAgent(ScriptedLLM(_read_then_finish_script()), FakeWiki(), cfg)
    trace = agent.run(Task("Where was Alan Turing born?", language="en"))
    assert agent.has_grounded(trace) is True
    assert trace.grounding_rejections == 0
    assert trace.sufficiency.get("met") is True
    assert trace.voluntary_finish is True


def test_ungrounded_finish_takes_the_same_path_on_the_last_step():
    cfg = Config(backend="groq", max_steps=1)
    scripted = [
        '{"sub_questions":[],"stop_criterion":"x","plan":"y"}',
        '{"thought":"guess","sufficiency_note":"met","action":"finish","action_input":'
        '{"answer":"London","sufficiency":{"met":true,"confidence":1.0,"justification":"I know it"}}}',
    ]
    agent = DeepResearchAgent(ScriptedLLM(scripted), FakeWiki(), cfg)
    trace = agent.run(Task("Where was Alan Turing born?", language="en"))
    assert trace.stopped_reason == "agent called finish"
    assert trace.grounding_rejections == 0
    assert trace.sufficiency.get("met") is False
    assert "grounding gate" in trace.sufficiency.get("justification", "")


class TelemetryLLM(ScriptedLLM):
    def __init__(self, scripted):
        super().__init__(scripted)
        self.last_model = ""
        self.last_json_mode = ""
        self.total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    def reset_usage(self):
        self.calls = 0
        self.total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    def chat(self, messages, temperature=None, max_tokens=None, force_json=False):
        self.last_model = "GigaChat-2-Max:1.0.0"
        self.last_json_mode = "native"
        self.total_usage["prompt_tokens"] += 100
        self.total_usage["completion_tokens"] += 20
        self.total_usage["total_tokens"] += 120
        return super().chat(messages, temperature, max_tokens, force_json)


def test_trace_records_responding_model_tokens_and_gold():
    cfg = Config(backend="gigachat", max_steps=3)
    llm = TelemetryLLM(_read_then_finish_script())
    agent = DeepResearchAgent(llm, FakeWiki(), cfg)
    trace = agent.run(Task("Where was Alan Turing born?", language="en",
                           gold=["London", "Maida Vale"]))
    assert trace.model == "GigaChat-2-Max"
    assert trace.resolved_model == "GigaChat-2-Max:1.0.0"
    assert trace.json_mode == "native"
    assert trace.llm_calls == 3
    assert trace.token_usage["total_tokens"] == 360
    assert trace.gold == ["London", "Maida Vale"]
    md = trace.to_markdown()
    assert "differs from the requested identifier" in md
    assert "Reference (gold)" in md


def test_section_name_is_resolved_to_an_index():
    scripted = [
        '{"sub_questions":[],"stop_criterion":"x","plan":"y"}',
        '{"thought":"read","sufficiency_note":"n/a","action":"read_section",'
        '"action_input":{"title":"Alan Turing","section":"Education"}}',
        '{"thought":"done","sufficiency_note":"met","action":"finish","action_input":'
        '{"answer":"King\'s College","sufficiency":{"met":true,"confidence":0.9,"justification":"j"}}}',
    ]
    cfg = Config(backend="groq", max_steps=3)
    agent = DeepResearchAgent(ScriptedLLM(scripted), FakeWiki(), cfg)
    trace = agent.run(Task("Where did Turing study?", language="en"))
    assert not trace.steps[0].observation.startswith("Tool error")
    assert agent.has_grounded(trace) is True
    assert trace.sources[0]["section"] == "1"


def test_unknown_section_name_errors_with_the_valid_indices_listed():
    scripted = [
        '{"sub_questions":[],"stop_criterion":"x","plan":"y"}',
        '{"thought":"read","sufficiency_note":"n/a","action":"read_section",'
        '"action_input":{"title":"Alan Turing","section":"Nonexistent heading"}}',
        '{"thought":"done","sufficiency_note":"n/a","action":"finish","action_input":'
        '{"answer":"x","sufficiency":{"met":true}}}',
    ]
    cfg = Config(backend="groq", max_steps=3)
    agent = DeepResearchAgent(ScriptedLLM(scripted), FakeWiki(), cfg)
    trace = agent.run(Task("q", language="en"))
    obs = trace.steps[0].observation
    assert obs.startswith("Tool error")
    assert "[0] Lead" in obs and "[1] Education" in obs


def test_bracketed_section_index_is_accepted():
    scripted = [
        '{"sub_questions":[],"stop_criterion":"x","plan":"y"}',
        '{"thought":"read","sufficiency_note":"n/a","action":"read_section",'
        '"action_input":{"title":"Alan Turing","section":"[1]"}}',
        '{"thought":"done","sufficiency_note":"met","action":"finish","action_input":'
        '{"answer":"King\'s College","sufficiency":{"met":true,"confidence":0.9,"justification":"j"}}}',
    ]
    cfg = Config(backend="groq", max_steps=3)
    agent = DeepResearchAgent(ScriptedLLM(scripted), FakeWiki(), cfg)
    trace = agent.run(Task("q", language="en"))
    assert not trace.steps[0].observation.startswith("Tool error")
    assert trace.sources[0]["section"] == "1"
