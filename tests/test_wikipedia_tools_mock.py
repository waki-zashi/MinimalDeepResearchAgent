import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wikipedia_tools import WikipediaClient, html_to_text


def test_html_to_text_basic():
    html = ("<div><p>Hello <b>world</b>.</p>"
            "<sup class='reference'>[1]</sup><p>Second line.</p></div>")
    txt = html_to_text(html)
    assert "Hello world." in txt
    assert "[1]" not in txt
    assert "Second line." in txt


def test_search_parsing(monkeypatch):
    c = WikipediaClient()
    monkeypatch.setattr(c, "_get", lambda params, lang=None: {
        "query": {"search": [
            {"title": "Alan Turing", "snippet": "English <b>mathematician</b>"}]}})
    res = c.search("turing")
    assert res[0]["title"] == "Alan Turing"
    assert "mathematician" in res[0]["snippet"]


def test_sections_prepends_lead(monkeypatch):
    c = WikipediaClient()
    monkeypatch.setattr(c, "_get", lambda params, lang=None: {
        "parse": {"title": "Alan Turing",
                  "sections": [{"index": "1", "level": "2", "line": "Education"}]}})
    secs = c.get_sections("Alan Turing")
    assert secs["sections"][0]["index"] == "0"
    assert any(s["line"] == "Education" for s in secs["sections"])


def test_read_section(monkeypatch):
    c = WikipediaClient()
    monkeypatch.setattr(c, "_get", lambda params, lang=None: {
        "parse": {"title": "Alan Turing",
                  "text": {"*": "<p>Turing studied at King's College, Cambridge.</p>"}}})
    rd = c.read_section("Alan Turing", "1")
    assert "King's College" in rd["text"]
    assert rd["truncated"] is False


def test_read_section_truncation(monkeypatch):
    c = WikipediaClient()
    long_html = "<p>" + ("word " * 1000) + "</p>"
    monkeypatch.setattr(c, "_get", lambda params, lang=None: {
        "parse": {"title": "X", "text": {"*": long_html}}})
    rd = c.read_section("X", "0", char_limit=100)
    assert rd["truncated"] is True
    assert len(rd["text"]) == 100


def test_read_section_detects_redirect(monkeypatch):
    c = WikipediaClient()
    monkeypatch.setattr(c, "_get", lambda params, lang=None: {
        "parse": {"title": "Alan Turing",
                  "text": {"*": "<p>Turing studied at King's College, Cambridge.</p>"}}})
    rd = c.read_section("Alan M. Turing", "1")
    assert rd["title"] == "Alan Turing"
    assert rd["requested_title"] == "Alan M. Turing"
    assert rd["redirected"] is True


def test_read_section_no_redirect_when_title_matches(monkeypatch):
    c = WikipediaClient()
    monkeypatch.setattr(c, "_get", lambda params, lang=None: {
        "parse": {"title": "Alan_Turing",
                  "text": {"*": "<p>Text.</p>"}}})
    rd = c.read_section("Alan Turing", "0")
    assert rd["redirected"] is False


def test_get_retries_on_429_then_succeeds(monkeypatch):
    c = WikipediaClient(min_interval=0.0)
    monkeypatch.setattr("wikipedia_tools.time.sleep", lambda s: None)

    calls = {"n": 0}

    class FakeResp:
        def __init__(self, status_code, body):
            self.status_code = status_code
            self.text = body
            self.headers = {}

        def json(self):
            return {"ok": True}

    def fake_get(url, params=None, timeout=None):
        calls["n"] += 1
        if calls["n"] < 3:
            return FakeResp(429, "rate limited")
        return FakeResp(200, "{}")

    monkeypatch.setattr(c.session, "get", fake_get)
    data = c._get({"action": "query"})
    assert data == {"ok": True}
    assert calls["n"] == 3
