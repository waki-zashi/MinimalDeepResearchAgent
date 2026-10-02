import concurrent.futures
import os
import socket
import ssl
import time

import requests

from config import load_dotenv

_EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=4)


def dns_check(host):
    t0 = time.time()
    try:
        ip = socket.gethostbyname(host)
        return True, time.time() - t0, ip
    except Exception as e:
        return False, time.time() - t0, f"{type(e).__name__}: {e}"


def tcp_check(host, port, timeout=5):
    t0 = time.time()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True, time.time() - t0, None
    except Exception as e:
        return False, time.time() - t0, f"{type(e).__name__}: {e}"


def tls_check(host, port, timeout=5):
    t0 = time.time()
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as tls_sock:
                cert = tls_sock.getpeercert()
                issuer = dict(x[0] for x in cert.get("issuer", []))
                return True, time.time() - t0, issuer.get("organizationName", issuer)
    except Exception as e:
        return False, time.time() - t0, f"{type(e).__name__}: {e}"


def watchdog_request(method, url, hard_timeout, **kwargs):
    t0 = time.time()
    fut = _EXECUTOR.submit(requests.request, method, url, **kwargs)
    try:
        r = fut.result(timeout=hard_timeout)
        return "OK", time.time() - t0, r
    except concurrent.futures.TimeoutError:
        return "HARD_HANG", time.time() - t0, None
    except requests.exceptions.ConnectTimeout as e:
        return "CONNECT_TIMEOUT", time.time() - t0, str(e)
    except requests.exceptions.ReadTimeout as e:
        return "READ_TIMEOUT", time.time() - t0, str(e)
    except requests.exceptions.ProxyError as e:
        return "PROXY_ERROR", time.time() - t0, str(e)
    except requests.exceptions.SSLError as e:
        return "SSL_ERROR", time.time() - t0, str(e)
    except requests.exceptions.ConnectionError as e:
        return "CONNECTION_ERROR", time.time() - t0, str(e)
    except Exception as e:
        return f"OTHER_{type(e).__name__}", time.time() - t0, str(e)


def report_http(label, status, elapsed, extra, request_timeout):
    print(f"  [{label}] {status} after {elapsed:.2f}s", flush=True)
    if status == "OK":
        r = extra
        print(f"      http_status={r.status_code} body[:300]={r.text[:300]!r}", flush=True)
    elif status == "HARD_HANG":
        print(f"      requests' own timeout={request_timeout}s did NOT fire within "
              f"{elapsed:.2f}s - the call is truly stuck below the HTTP layer "
              f"(a TLS-inspecting proxy/firewall/antivirus holding the socket open is the "
              f"usual cause on Windows).", flush=True)
    else:
        print(f"      {extra}", flush=True)
    print(flush=True)


def section(title):
    print(f"\n=== {title} ===", flush=True)


def main():
    load_dotenv()
    groq_key = os.environ.get("GROQ_API_KEY")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    gigachat_key = os.environ.get("GIGACHAT_AUTH_KEY")

    targets = [
        ("api.groq.com", 443),
        ("generativelanguage.googleapis.com", 443),
        ("ngw.devices.sberbank.ru", 9443),
        ("en.wikipedia.org", 443),
    ]

    section("DNS")
    for host, _ in targets:
        ok, dt, info = dns_check(host)
        print(f"  {host}: {'OK' if ok else 'FAIL'} ({dt:.2f}s) -> {info}", flush=True)

    section("TCP connect")
    for host, port in targets:
        ok, dt, info = tcp_check(host, port)
        print(f"  {host}:{port}: {'OK' if ok else 'FAIL'} ({dt:.2f}s) {info or ''}", flush=True)

    section("TLS handshake + certificate issuer")
    for host, port in targets:
        ok, dt, info = tls_check(host, port)
        print(f"  {host}:{port}: {'OK' if ok else 'FAIL'} ({dt:.2f}s) issuer={info}", flush=True)

    section("Groq: minimal chat completion (no json mode, no reasoning)")
    if not groq_key:
        print("  GROQ_API_KEY missing, skipping", flush=True)
    else:
        status, elapsed, extra = watchdog_request(
            "POST", "https://api.groq.com/openai/v1/chat/completions",
            hard_timeout=40,
            headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
            json={"model": "openai/gpt-oss-120b",
                 "messages": [{"role": "user", "content": "Say OK."}],
                 "max_tokens": 16},
            timeout=20)
        report_http("groq/plain", status, elapsed, extra, 20)

    section("Groq: chat completion WITH json_object + reasoning_effort=low (repro of agent's real call)")
    if not groq_key:
        print("  GROQ_API_KEY missing, skipping", flush=True)
    else:
        status, elapsed, extra = watchdog_request(
            "POST", "https://api.groq.com/openai/v1/chat/completions",
            hard_timeout=90,
            headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
            json={"model": "openai/gpt-oss-120b",
                 "messages": [{"role": "user",
                              "content": 'Reply with exactly this JSON and nothing else: {"ok": true}'}],
                 "max_tokens": 300,
                 "response_format": {"type": "json_object"},
                 "reasoning_effort": "low",
                 "reasoning_format": "hidden"},
            timeout=60)
        report_http("groq/json_object+reasoning", status, elapsed, extra, 60)

    section("Gemini: minimal generateContent")
    if not gemini_key:
        print("  GEMINI_API_KEY missing, skipping", flush=True)
    else:
        status, elapsed, extra = watchdog_request(
            "POST",
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent",
            hard_timeout=40,
            headers={"Content-Type": "application/json", "x-goog-api-key": gemini_key},
            json={"contents": [{"role": "user", "parts": [{"text": "Say OK."}]}],
                 "generationConfig": {"maxOutputTokens": 16}},
            timeout=20)
        report_http("gemini/plain", status, elapsed, extra, 20)

    section("GigaChat: OAuth token request")
    giga_token = None
    if not gigachat_key:
        print("  GIGACHAT_AUTH_KEY missing, skipping", flush=True)
    else:
        import uuid
        status, elapsed, extra = watchdog_request(
            "POST", "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
            hard_timeout=40,
            headers={"Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json",
                    "RqUID": str(uuid.uuid4()),
                    "Authorization": f"Basic {gigachat_key}"},
            data={"scope": "GIGACHAT_API_PERS"},
            timeout=20, verify=False)
        report_http("gigachat/oauth", status, elapsed, extra, 20)
        if status == "OK" and extra is not None and extra.status_code == 200:
            giga_token = extra.json().get("access_token")

    section("GigaChat: minimal chat completion")
    if not giga_token:
        print("  no access token from previous step, skipping", flush=True)
    else:
        status, elapsed, extra = watchdog_request(
            "POST", "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
            hard_timeout=40,
            headers={"Authorization": f"Bearer {giga_token}", "Content-Type": "application/json"},
            json={"model": "GigaChat",
                 "messages": [{"role": "user", "content": "Say OK."}],
                 "max_tokens": 16},
            timeout=20, verify=False)
        report_http("gigachat/chat", status, elapsed, extra, 20)

    print("Done.", flush=True)


if __name__ == "__main__":
    main()
