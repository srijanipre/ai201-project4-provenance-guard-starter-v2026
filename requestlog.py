"""
request log (unit 9)

writes one json line per http request (any route) to logs/requests.jsonl.

this is NOT the audit log. audit.py has the decisions (scores, labels,
appeals, rejections) with the 9 fields from unit 8. this one is more about
how the service itself is doing - how long stuff took, what status went
back, input/output size, and what broke if something broke. kept them
seperate so the audit log schema doesnt change.

never writes the submitted text, just how long it is.

    from requestlog import init_app
    init_app(app)        # right after app = Flask(...)

to read it:

    python requestlog.py            # last 10 lines
    python requestlog.py 25         # last 25
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

# dont bother parsing responses bigger than this. GET /log can get huge and
# the size is all we care about there anyway
_MAX_PARSE_BYTES = 64 * 1024


def init_app(app) -> None:
    """
    hooks the request log into the app.

    has to be called before the rate limiter gets set up - flask runs
    before_request hooks in order, so if the limiter goes first a 429 never
    gets a start time.
    """
    app.before_request(_start)
    app.after_request(_finish)


def note_exception(exc: BaseException) -> None:
    """save the exception so the 500 line can say what it was"""
    g._reqlog_exception = exc


def _start() -> None:
    g._reqlog_t0 = time.perf_counter()
    g._reqlog_ts = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
    # false = this request has to load gpt2 first (cold), true = warm
    g._reqlog_model_loaded = detector._model is not None


def _finish(response):
    try:
        write(build_entry(response))
    except Exception as exc:  # noqa: BLE001
        # if logging breaks, dont turn a good response into a 500
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
        # flasks own 404/405 pages are html, no error key
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
    """read the log back, oldest first. skips bad lines"""
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
