import os
from dataclasses import dataclass


def load_dotenv(path=".env"):
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


@dataclass
class Config:
    backend: str = "groq"
    groq_model: str = "openai/gpt-oss-120b"
    gemini_model: str = "gemini-flash-latest"
    gemini_thinking_budget: int = 0
    gigachat_model: str = "GigaChat-2-Max"
    gigachat_scope: str = "GIGACHAT_API_PERS"
    gigachat_verify_ssl: bool = False
    gigachat_native_json: bool = True
    language: str = "en"
    max_steps: int = 12
    temperature: float = 0.2
    max_tokens: int = 6144
    groq_reasoning_effort: str = "low"
    obs_char_limit: int = 1500
    search_limit: int = 5
    min_grounding_chars: int = 32
    request_timeout: int = 30
    reports_dir: str = "reports"
    force_json: bool = True
    relevance_gate: bool = False

    @property
    def model(self):
        if self.backend == "groq":
            return self.groq_model
        if self.backend == "gigachat":
            return self.gigachat_model
        return self.gemini_model
