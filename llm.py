import concurrent.futures
import json
import os
import re
import time
import uuid

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=4)


class LLMError(Exception):
    pass


def _zero_usage():
    return {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}


class LLM:
    def __init__(self, config):
        self.cfg = config
        self.backend = config.backend
        self._gigachat_token = None
        self._gigachat_token_expires_at = 0
        self._giga_native_confirmed = False
        self.last_model = ""
        self.last_usage = {}
        self.last_json_mode = ""
        self.total_usage = _zero_usage()
        self.calls = 0
        if self.backend == "groq":
            self.api_key = os.environ.get("GROQ_API_KEY")
        elif self.backend == "gemini":
            self.api_key = os.environ.get("GEMINI_API_KEY")
        elif self.backend == "gigachat":
            self.api_key = os.environ.get("GIGACHAT_AUTH_KEY")
        else:
            raise LLMError(f"Unknown backend: {self.backend}")
        if not self.api_key:
            raise LLMError(f"Missing API key for backend '{self.backend}'")

    def reset_usage(self):
        self.total_usage = _zero_usage()
        self.calls = 0
        self.last_model = ""
        self.last_usage = {}
        self.last_json_mode = ""

    def _note_call(self, model, usage, json_mode):
        usage = usage or {}
        self.last_model = model or self.cfg.model
        self.last_usage = usage
        self.last_json_mode = json_mode
        self.calls += 1
        p = int(usage.get("prompt_tokens", usage.get("promptTokenCount", 0)) or 0)
        c = int(usage.get("completion_tokens", usage.get("candidatesTokenCount", 0)) or 0)
        extra = int(usage.get("thoughtsTokenCount", 0) or 0)
        t = int(usage.get("total_tokens", usage.get("totalTokenCount", 0)) or 0)
        if not t:
            t = p + c + extra
        self.total_usage["prompt_tokens"] += p
        self.total_usage["completion_tokens"] += c + extra
        self.total_usage["total_tokens"] += t

    def chat(self, messages, temperature=None, max_tokens=None, force_json=False):
        t = self.cfg.temperature if temperature is None else temperature
        mt = self.cfg.max_tokens if max_tokens is None else max_tokens
        if self.backend == "groq":
            return self._groq(messages, t, mt, force_json)
        if self.backend == "gigachat":
            return self._giga(messages, t, mt, force_json)
        return self._gemini(messages, t, mt, force_json)

    def _post(self, url, headers, payload, verify=True, data=None):
        last = None
        for attempt in range(5):
            try:
                kwargs = {"headers": headers, "timeout": self.cfg.request_timeout,
                          "verify": verify}
                if data is not None:
                    kwargs["data"] = data
                else:
                    kwargs["json"] = payload
                fut = _EXECUTOR.submit(requests.post, url, **kwargs)
                r = fut.result(timeout=self.cfg.request_timeout + 10)
            except (requests.RequestException, concurrent.futures.TimeoutError) as e:
                last = e
                time.sleep(1.5 * (attempt + 1))
                continue
            if r.status_code == 200:
                return r.json()
            if r.status_code == 429:
                last = LLMError(f"429: {r.text[:200]}")
                time.sleep(self._retry_wait(r))
                continue
            if r.status_code in (500, 502, 503, 529):
                last = LLMError(f"{r.status_code}: {r.text[:200]}")
                time.sleep(2.0 * (attempt + 1))
                continue
            raise LLMError(f"{r.status_code}: {r.text[:300]}")
        raise LLMError(f"Request failed after retries: {last}")

    def _retry_wait(self, r):
        ra = r.headers.get("Retry-After")
        if ra:
            try:
                return float(ra) + 0.5
            except ValueError:
                pass
        m = re.search(r"try again in ([\d.]+)s", r.text or "", re.IGNORECASE)
        if m:
            return float(m.group(1)) + 0.5
        return 20.0

    def _groq(self, messages, temperature, max_tokens, force_json):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}",
                   "Content-Type": "application/json"}
        payload = {"model": self.cfg.groq_model, "messages": messages,
                   "temperature": temperature, "max_tokens": max_tokens}
        if force_json:
            payload["response_format"] = {"type": "json_object"}
        if "gpt-oss" in self.cfg.groq_model and self.cfg.groq_reasoning_effort:
            payload["reasoning_effort"] = self.cfg.groq_reasoning_effort
            payload["reasoning_format"] = "hidden"
        try:
            data = self._post(url, headers, payload)
        except LLMError as e:
            if "json_validate_failed" in str(e) and "response_format" in payload:
                payload.pop("response_format")
                data = self._post(url, headers, payload)
            else:
                raise
        self._note_call(data.get("model"), data.get("usage", {}),
                        "native" if "response_format" in payload else "post-hoc repair")
        return data["choices"][0]["message"]["content"]

    def _gemini(self, messages, temperature, max_tokens, force_json):
        model = self.cfg.gemini_model
        url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
               f"{model}:generateContent")
        headers = {"Content-Type": "application/json", "x-goog-api-key": self.api_key}
        system_texts = [m["content"] for m in messages if m["role"] == "system"]
        contents = []
        for m in messages:
            if m["role"] == "system":
                continue
            role = "user" if m["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": m["content"]}]})
        gen = {"temperature": temperature, "maxOutputTokens": max_tokens,
              "thinkingConfig": {"thinkingBudget": self.cfg.gemini_thinking_budget}}
        if force_json:
            gen["responseMimeType"] = "application/json"
        payload = {"contents": contents, "generationConfig": gen}
        if system_texts:
            payload["systemInstruction"] = {"parts": [{"text": "\n\n".join(system_texts)}]}
        data = self._post(url, headers, payload)
        self._note_call(data.get("modelVersion"), data.get("usageMetadata", {}),
                        "native" if force_json else "post-hoc repair")
        cands = data.get("candidates", [])
        if not cands:
            raise LLMError(f"No candidates returned: {json.dumps(data)[:300]}")
        cand = cands[0]
        parts = cand.get("content", {}).get("parts", [])
        text = "".join(part.get("text", "") for part in parts)
        if not text:
            raise LLMError(f"Empty content, finishReason={cand.get('finishReason')}: "
                          f"{json.dumps(data)[:300]}")
        return text

    def _giga_auth(self):
        now = time.time()
        if self._gigachat_token and now < self._gigachat_token_expires_at - 30:
            return self._gigachat_token
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Accept": "application/json",
                   "RqUID": str(uuid.uuid4()),
                   "Authorization": f"Basic {self.api_key}"}
        data = self._post(url, headers, None, verify=self.cfg.gigachat_verify_ssl,
                          data={"scope": self.cfg.gigachat_scope})
        self._gigachat_token = data["access_token"]
        self._gigachat_token_expires_at = self._normalize_expiry(data.get("expires_at"), now)
        return self._gigachat_token

    @staticmethod
    def _normalize_expiry(expires_at, now, default_ttl=1800):
        """GigaChat returns expires_at as a Unix timestamp in MILLISECONDS. Comparing it
        against time.time() (seconds) makes every token look valid forever, so a batch
        running longer than the real 30-minute lifetime dies on 401 instead of refreshing."""
        try:
            ts = float(expires_at)
        except (TypeError, ValueError):
            return now + default_ttl
        if ts > 1e11:
            ts /= 1000.0
        if ts <= now:
            return now + default_ttl
        return ts

    def _giga(self, messages, temperature, max_tokens, force_json):
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        payload = {"model": self.cfg.gigachat_model, "messages": messages,
                   "temperature": temperature, "max_tokens": max_tokens}
        native = bool(force_json and self.cfg.gigachat_native_json)
        if native:
            payload["response_format"] = {"type": "json_object"}

        def send():
            token = self._giga_auth()
            headers = {"Authorization": f"Bearer {token}",
                       "Content-Type": "application/json"}
            return self._post(url, headers, payload,
                              verify=self.cfg.gigachat_verify_ssl)

        try:
            data = send()
        except LLMError as e:
            if "401" in str(e):
                self._gigachat_token = None
                self._gigachat_token_expires_at = 0
                data = send()
            elif native and not self._giga_native_confirmed:
                self.cfg.gigachat_native_json = False
                payload.pop("response_format", None)
                native = False
                data = send()
            else:
                raise
        if native:
            self._giga_native_confirmed = True
        self._note_call(data.get("model"), data.get("usage", {}),
                        "native" if native else "post-hoc repair")
        return data["choices"][0]["message"]["content"]
