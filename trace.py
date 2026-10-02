import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone


@dataclass
class Step:
    n: int
    thought: str = ""
    action: str = ""
    action_input: dict = field(default_factory=dict)
    observation: str = ""
    sufficiency_note: str = ""


@dataclass
class Trace:
    question: str
    language: str
    backend: str
    model: str
    stop_criterion: str = ""
    stop_criterion_source: str = ""
    sub_questions: list = field(default_factory=list)
    plan: str = ""
    steps: list = field(default_factory=list)
    final_answer: str = ""
    sufficiency: dict = field(default_factory=dict)
    sources: list = field(default_factory=list)
    started_at: str = ""
    finished_at: str = ""
    elapsed_sec: float = 0.0
    stopped_reason: str = ""
    voluntary_finish: bool = True
    relevance_checked: bool = False

    def to_dict(self):
        d = asdict(self)
        d["steps"] = [asdict(s) if not isinstance(s, dict) else s for s in self.steps]
        return d

    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    def to_markdown(self):
        L = []
        L.append(f"# Deep Research trace: {self.question}\n")
        L.append(f"- Language: `{self.language}`  ")
        L.append(f"- Backend / model: `{self.backend}` / `{self.model}`  ")
        L.append(f"- Started (UTC): {self.started_at}  ")
        L.append(f"- Elapsed: {self.elapsed_sec:.1f} s  ")
        L.append(f"- Steps: {len(self.steps)}  ")
        L.append(f"- Stopped: {self.stopped_reason}  ")
        L.append(f"- Voluntary finish: {self.voluntary_finish}  ")
        L.append(f"- Relevance-checked: {self.relevance_checked}\n")
        L.append("## Stopping criterion")
        L.append(f"_{self.stop_criterion_source}_: {self.stop_criterion}\n")
        if self.sub_questions:
            L.append("## Sub-questions")
            L += [f"- {q}" for q in self.sub_questions]
            L.append("")
        if self.plan:
            L.append("## Initial plan")
            L.append(self.plan + "\n")
        L.append("## Reasoning trace")
        for s in self.steps:
            L.append(f"### Step {s.n} — action: `{s.action}`")
            if s.thought:
                L.append(f"**Thought:** {s.thought}")
            if s.action_input:
                L.append(f"**Action input:** `{json.dumps(s.action_input, ensure_ascii=False)}`")
            if s.sufficiency_note:
                L.append(f"**Sufficiency note:** {s.sufficiency_note}")
            if s.observation:
                L.append("**Observation:**\n\n> " + s.observation.replace("\n", "\n> "))
            L.append("")
        L.append("## Final answer")
        L.append((self.final_answer or "(none)") + "\n")
        L.append("## Sufficiency judgment")
        if self.sufficiency:
            L.append(f"- Met: **{self.sufficiency.get('met')}**")
            if "confidence" in self.sufficiency:
                L.append(f"- Confidence: {self.sufficiency.get('confidence')}")
            L.append(f"- Justification: {self.sufficiency.get('justification', '')}")
        L.append("\n## Sources (provenance)")
        if self.sources:
            for src in self.sources:
                redirect_note = (f" (redirected from '{src.get('requested_title')}')"
                                 if src.get("redirected") else "")
                L.append(f"- [{src['lang']}] {src['title']}{redirect_note} — "
                        f"section {src['section']} — {src['url']}")
        else:
            L.append("- (none read)")
        L.append("")
        return "\n".join(L)


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")