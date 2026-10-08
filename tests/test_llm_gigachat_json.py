import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from config import Config
from llm import LLM, LLMError


def _giga_llm(monkeypatch, **cfg_kwargs):
    monkeypatch.setenv("GIGACHAT_AUTH_KEY", "dGVzdA==")
    llm = LLM(Config(backend="gigachat", **cfg_kwargs))
    monkeypatch.setattr(llm, "_giga_auth", lambda: "token")
    return llm


def _ok(content="{}", model="GigaChat-2-Max:1.0.0", usage=None):
    return {"model": model, "usage": usage or {"prompt_tokens": 10, "completion_tokens": 2,
                                               "total_tokens": 12},
            "choices": [{"message": {"content": content}}]}


def test_gigachat_requests_native_json_mode(monkeypatch):
    llm = _giga_llm(monkeypatch)
    seen = []

    def fake_post(url, headers, payload, verify=True, data=None):
        seen.append(payload)
        return _ok('{"a":1}')

    monkeypatch.setattr(llm, "_post", fake_post)
    out = llm.chat([{"role": "user", "content": "hi"}], force_json=True)
    assert out == '{"a":1}'
    assert seen[0]["response_format"] == {"type": "json_object"}
    assert seen[0]["model"] == "GigaChat-2-Max"
    assert llm.last_json_mode == "native"
    assert llm.last_model == "GigaChat-2-Max:1.0.0"
    assert llm.total_usage["total_tokens"] == 12
    assert llm.calls == 1


def test_gigachat_falls_back_when_response_format_is_rejected(monkeypatch):
    llm = _giga_llm(monkeypatch)
    seen = []

    def fake_post(url, headers, payload, verify=True, data=None):
        seen.append(dict(payload))
        if "response_format" in payload:
            raise LLMError('422: {"message":"Unknown field response_format"}')
        return _ok("free text")

    monkeypatch.setattr(llm, "_post", fake_post)
    out = llm.chat([{"role": "user", "content": "hi"}], force_json=True)
    assert out == "free text"
    assert len(seen) == 2
    assert "response_format" in seen[0] and "response_format" not in seen[1]
    assert llm.last_json_mode == "post-hoc repair"
    assert llm.cfg.gigachat_native_json is False


def test_gigachat_does_not_probe_again_after_a_rejection(monkeypatch):
    llm = _giga_llm(monkeypatch)
    seen = []

    def fake_post(url, headers, payload, verify=True, data=None):
        seen.append(dict(payload))
        if "response_format" in payload:
            raise LLMError("400: bad field")
        return _ok("ok")

    monkeypatch.setattr(llm, "_post", fake_post)
    llm.chat([{"role": "user", "content": "a"}], force_json=True)
    llm.chat([{"role": "user", "content": "b"}], force_json=True)
    assert sum(1 for p in seen if "response_format" in p) == 1


def test_gigachat_propagates_errors_once_native_mode_is_confirmed(monkeypatch):
    llm = _giga_llm(monkeypatch)
    calls = {"n": 0}

    def fake_post(url, headers, payload, verify=True, data=None):
        calls["n"] += 1
        if calls["n"] == 1:
            return _ok("{}")
        raise LLMError("429: rate limited")

    monkeypatch.setattr(llm, "_post", fake_post)
    llm.chat([{"role": "user", "content": "a"}], force_json=True)
    with pytest.raises(LLMError):
        llm.chat([{"role": "user", "content": "b"}], force_json=True)
    assert calls["n"] == 2


def test_reset_usage_clears_counters(monkeypatch):
    llm = _giga_llm(monkeypatch)
    monkeypatch.setattr(llm, "_post",
                        lambda url, headers, payload, verify=True, data=None: _ok("{}"))
    llm.chat([{"role": "user", "content": "a"}], force_json=True)
    llm.reset_usage()
    assert llm.calls == 0
    assert llm.total_usage["total_tokens"] == 0
    assert llm.last_model == ""


def test_millisecond_expiry_is_normalized_to_seconds():
    now = 1_790_000_000.0
    assert LLM._normalize_expiry(1_790_001_800_000, now) == 1_790_001_800.0
    assert LLM._normalize_expiry(now + 1800, now) == now + 1800
    assert LLM._normalize_expiry(None, now) == now + 1800
    assert LLM._normalize_expiry(now - 10, now) == now + 1800


def test_token_is_refreshed_once_on_401_instead_of_failing_the_run(monkeypatch):
    monkeypatch.setenv("GIGACHAT_AUTH_KEY", "dGVzdA==")
    llm = LLM(Config(backend="gigachat"))
    auths = {"n": 0}

    def fake_auth():
        auths["n"] += 1
        return f"token{auths['n']}"

    monkeypatch.setattr(llm, "_giga_auth", fake_auth)
    seen = []

    def fake_post(url, headers, payload, verify=True, data=None):
        seen.append(headers["Authorization"])
        if len(seen) == 1:
            raise LLMError('401: {"status":401,"message":"Token has expired"}')
        return _ok("{}")

    monkeypatch.setattr(llm, "_post", fake_post)
    out = llm.chat([{"role": "user", "content": "hi"}], force_json=True)
    assert out == "{}"
    assert seen == ["Bearer token1", "Bearer token2"]


def test_expired_token_is_dropped_from_the_cache_on_401(monkeypatch):
    monkeypatch.setenv("GIGACHAT_AUTH_KEY", "dGVzdA==")
    llm = LLM(Config(backend="gigachat"))
    llm._gigachat_token = "stale"
    llm._gigachat_token_expires_at = 9e18
    calls = {"n": 0}

    def fake_post(url, headers, payload, verify=True, data=None):
        calls["n"] += 1
        if calls["n"] == 1:
            raise LLMError("401: Token has expired")
        if "oauth" in url:
            return {"access_token": "fresh", "expires_at": 1_790_001_800_000}
        return _ok("{}")

    monkeypatch.setattr(llm, "_post", fake_post)
    llm.chat([{"role": "user", "content": "hi"}], force_json=True)
    assert llm._gigachat_token == "fresh"
