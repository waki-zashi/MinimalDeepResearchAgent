import concurrent.futures
import re
import time
from html.parser import HTMLParser

import requests

_EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=4)

_BLOCK = {"p", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6",
          "div", "br", "ul", "ol", "dd", "dt"}
_SKIP = {"script", "style", "sup", "table"}


class _Stripper(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in _SKIP:
            self.skip_depth += 1
        elif tag in _BLOCK:
            self.parts.append("\n")

    def handle_startendtag(self, tag, attrs):
        if tag in _BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in _SKIP and self.skip_depth > 0:
            self.skip_depth -= 1
        elif tag in _BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.skip_depth == 0:
            self.parts.append(data)

    def text(self):
        t = "".join(self.parts)
        t = re.sub(r"\[edit\]", "", t)
        t = re.sub(r"[ \t]+", " ", t)
        t = re.sub(r"\n\s*\n\s*\n+", "\n\n", t)
        return t.strip()


def html_to_text(s):
    p = _Stripper()
    p.feed(s)
    return p.text()


class WikipediaError(Exception):
    pass


class WikipediaClient:
    def __init__(self, language="en", timeout=30,
                 user_agent="DeepResearchWikiMVP/1.0 (research prototype)",
                 min_interval=1.0):
        self.language = language
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})
        self._min_interval = min_interval
        self._last_ts = 0.0

    def _endpoint(self, lang=None):
        return f"https://{lang or self.language}.wikipedia.org/w/api.php"

    def _get(self, params, lang=None):
        params = dict(params)
        params["format"] = "json"
        last = None
        for attempt in range(4):
            wait = self._min_interval - (time.monotonic() - self._last_ts)
            if wait > 0:
                time.sleep(wait)
            try:
                fut = _EXECUTOR.submit(self.session.get, self._endpoint(lang), params=params,
                                       timeout=self.timeout)
                r = fut.result(timeout=self.timeout + 10)
            except concurrent.futures.TimeoutError:
                self._last_ts = time.monotonic()
                last = WikipediaError(f"hard timeout after {self.timeout + 10}s")
                continue
            except requests.RequestException as e:
                self._last_ts = time.monotonic()
                last = WikipediaError(str(e))
                continue
            self._last_ts = time.monotonic()
            if r.status_code == 429:
                retry_after = r.headers.get("Retry-After")
                try:
                    retry_wait = float(retry_after)
                except (TypeError, ValueError):
                    retry_wait = 2.0 * (attempt + 1)
                last = WikipediaError(f"HTTP 429: {r.text[:200]}")
                time.sleep(retry_wait)
                continue
            if r.status_code != 200:
                raise WikipediaError(f"HTTP {r.status_code}: {r.text[:200]}")
            return r.json()
        raise WikipediaError(f"rate-limited after retries: {last}")

    def search(self, query, limit=5, lang=None):
        data = self._get({"action": "query", "list": "search", "srsearch": query,
                          "srlimit": limit, "srprop": "snippet"}, lang)
        out = []
        for item in data.get("query", {}).get("search", []):
            out.append({"title": item["title"],
                        "snippet": html_to_text(item.get("snippet", ""))})
        return out

    def get_sections(self, title, lang=None):
        data = self._get({"action": "parse", "page": title, "prop": "sections",
                          "redirects": 1}, lang)
        if "error" in data:
            raise WikipediaError(data["error"].get("info", "parse error"))
        secs = data.get("parse", {}).get("sections", [])
        out = [{"index": "0", "level": "1", "line": "(Lead / introduction)"}]
        for s in secs:
            out.append({"index": s.get("index", ""), "level": s.get("level", ""),
                        "line": s.get("line", "")})
        return {"title": data.get("parse", {}).get("title", title), "sections": out}

    def read_section(self, title, section="0", lang=None, char_limit=None):
        data = self._get({"action": "parse", "page": title, "prop": "text",
                          "section": str(section), "redirects": 1,
                          "disabletoc": 1}, lang)
        if "error" in data:
            raise WikipediaError(data["error"].get("info", "parse error"))
        resolved = data.get("parse", {}).get("title", title)
        html_text = data.get("parse", {}).get("text", {}).get("*", "")
        text = html_to_text(html_text)
        truncated = False
        if char_limit and len(text) > char_limit:
            text = text[:char_limit]
            truncated = True

        def _norm(s):
            return re.sub(r"[\s_]+", " ", s).strip().lower()

        redirected = _norm(title) != _norm(resolved)
        return {"title": resolved, "requested_title": title, "redirected": redirected,
                "section": str(section), "text": text, "truncated": truncated}
