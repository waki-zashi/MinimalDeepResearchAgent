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
    resolved_model: str = ""
    json_mode: str = ""
    gold: object = None
    expect_abstention: bool = False
    repeat: int = 1
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
    relevance: dict = field(default_factory=dict)
    grounding_rejections: int = 0
    llm_calls: int = 0
    token_usage: dict = field(default_factory=dict)

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
        L.append(f"- Backend / requested model: `{self.backend}` / `{self.model}`  ")
        resolved = self.resolved_model or "(not reported)"
        mismatch = (" **(differs from the requested identifier — server-side redirect)**"
                    if self.resolved_model and self.resolved_model != self.model else "")
        L.append(f"- Model that actually answered: `{resolved}`{mismatch}  ")
        L.append(f"- JSON mode: {self.json_mode or 'n/a'}  ")
        L.append(f"- Started (UTC): {self.started_at}  ")
        L.append(f"- Elapsed: {self.elapsed_sec:.1f} s  ")
        L.append(f"- Steps: {len(self.steps)}  ")
        L.append(f"- Run (repeat index): {self.repeat}  ")
        L.append(f"- Stopped: {self.stopped_reason}  ")
        L.append(f"- Voluntary finish: {self.voluntary_finish}  ")
        L.append(f"- Grounding-gate rejections: {self.grounding_rejections}  ")
        L.append(f"- Relevance-checked: {self.relevance_checked}  ")
        if self.relevance:
            verdict = "supported" if self.relevance.get("supported") else "NOT supported"
            L.append(f"- Relevance judge: **{verdict}** over "
                     f"{self.relevance.get('observations', 0)} read passage(s) — "
                     f"{self.relevance.get('reasoning', '')}  ")
        if self.token_usage:
            u = self.token_usage
            L.append(f"- LLM calls: {self.llm_calls} — tokens: "
                     f"{u.get('total_tokens', 0)} total "
                     f"({u.get('prompt_tokens', 0)} prompt / "
                     f"{u.get('completion_tokens', 0)} completion)  ")
        if self.gold is not None or self.expect_abstention:
            gold = "(abstention expected)" if self.expect_abstention else (
                ", ".join(self.gold) if isinstance(self.gold, list) else str(self.gold))
            L.append(f"- Reference (gold): {gold}  ")
        L.append("")
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
