"""
The request log. UNIT 9.

One JSON line per HTTP request, to any route, in logs/requests.jsonl.

This is not the audit log. audit.py records *decisions*: scores, labels,
appeals and rejected submissions, with the nine fields Unit 8 grades. This file
records how the service behaved as a service: how long each request took, what
status it returned, how big the input and output were, and what went wrong
when something failed. The two are kept apart so the audit log's schema never
changes.

The submitted text is never written here. Only its length is.

    from requestlog import init_app
    init_app(app)        # call right after app = Flask(...)

Read it back with:

    python requestlog.py            # the last 10 lines
    python requestlog.py 25         # the last 25
"""

import json
import sys
import threading
import time
from datetime import datetime, timezone

from flask import g, request

import config
import detector

_lock = threading.Lock()

# Responses bigger than this aren't parsed for output fields. GET /log can be
# hundreds of KB, and its size is all that's worth recording.
_MAX_PARSE_BYTES = 64 * 1024


def init_app(app) -> None:
    """
    Hook the request log into a Flask app.

    Call this before anything else registers a before_request hook (the rate
    limiter does). Flask runs those hooks in order, and the timer has to start
    first or a 429 from the limiter would have no start time.
    """
    app.before_request(_start)
    app.after_request(_finish)


def note_exception(exc: BaseException) -> None:
    """Remember an unhandled exception so the 500's log line can name it."""
    g._reqlog_exception = exc


def _start() -> None:
    g._reqlog_t0 = time.perf_counter()
    g._reqlog_ts = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
    # False on the request that has to load gpt2 first, which is how a cold
    # request is told apart from a warm one.
    g._reqlog_model_loaded = detector._model is not None


def _finish(response):
    try:
        write(build_entry(response))
    except Exception as exc:  # noqa: BLE001
        # A logging failure must never turn a good response into a 500.
        print(f"[requestlog] could not write entry: {exc!r}", file=sys.stderr)
    return response


def build_entry(response) -> dict:
    t0 = g.get("_reqlog_t0")
    duration_ms = round((time.perf_counter() - t0) * 1000, 1) if t0 is not None else None

    payload = request.get_json(silent=True) if request.method == "POST" else None
    if not isinstance(payload, dict):
        payload = {}
    text = payload.get("text")
    creator = payload.get("creator_id")

    out_bytes = response.calculate_content_length()
    body = {}
    if response.is_json and out_bytes is not None and out_bytes <= _MAX_PARSE_BYTES:
        parsed = response.get_json(silent=True)
        body = parsed if isinstance(parsed, dict) else {}

    error = body.get("error")
    if error is None and response.status_code >= 400:
        # Flask's own 404 and 405 pages are HTML with no error key.
        error = f"http_{response.status_code}"

    exc = g.get("_reqlog_exception")
    content_id = body.get("content_id") or payload.get("content_id")

    return {
        "timestamp": g.get("_reqlog_ts") or datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        "method": request.method,
        "path": request.path,
        "status": response.status_code,
        "duration_ms": duration_ms,
        "in_bytes": request.content_length or 0,
        "in_text_chars": len(text) if isinstance(text, str) else None,
        "creator_id": creator[:200] if isinstance(creator, str) else None,
        "out_bytes": out_bytes,
        "content_id": content_id if isinstance(content_id, str) else None,
        "guess": body.get("guess"),
        "confidence": body.get("confidence"),
        "error": error,
        "exception": f"{type(exc).__name__}: {str(exc)[:200]}" if exc is not None else None,
        "model_loaded": g.get("_reqlog_model_loaded"),
    }


def write(entry: dict) -> None:
    config.REQUEST_LOG.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(entry, ensure_ascii=False)
    with _lock:
        with config.REQUEST_LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")


def read_entries(limit: int | None = None) -> list[dict]:
    """Read the request log back, oldest first. Bad lines are skipped."""
    if not config.REQUEST_LOG.exists():
        return []
    entries = []
    for line in config.REQUEST_LOG.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries[-limit:] if limit else entries


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    for e in read_entries(limit=n):
        print(json.dumps(e, ensure_ascii=False))
