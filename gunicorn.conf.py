"""
gunicorn settings for Provenance Guard. UNIT 9.

    gunicorn app:app            # picks this file up automatically

Each choice below is about the model, not about web traffic.
"""

import os

# Same variables as `python app.py`, so the same curl commands work either way.
bind = f"{os.getenv('HOST', '127.0.0.1')}:{os.getenv('PORT', '5000')}"

# One worker. Every worker loads its own copy of gpt2 (the measured memory is
# in the README), and the rate limiter keeps its counts in memory per process,
# so two workers would both double the RAM and let each caller through twice.
workers = 1
threads = 1

# The first request in a fresh worker loads gpt2 before it can score anything.
# gunicorn's default 30 s timeout would kill the worker on a slow machine in
# the middle of that load, so allow two minutes.
timeout = 120

# The app writes its own structured request log (logs/requests.jsonl), so
# gunicorn's text access log would only repeat it. Errors and tracebacks still
# go to the terminal.
accesslog = None
errorlog = "-"
loglevel = "info"


def post_worker_init(worker):
    """
    Unit 9 improvement: warm the model before the worker takes any requests.

    Without this, the first /submit after every start paid for loading gpt2
    *and* for torch's slow first forward pass (about 3.5 s + 3.7 s measured
    in-process), while /health already said "ok". Loading alone isn't enough,
    so this scores one passage long enough to fill the 400-token window.

    gunicorn is already listening while this runs, so early requests wait in
    the queue instead of failing. If the model can't load, the worker still
    starts and /submit answers 503 exactly as before.
    """
    import json
    import time
    from pathlib import Path

    import detector

    samples = json.loads((Path(__file__).parent / "samples" / "calibration.json").read_text(encoding="utf-8"))
    text = " ".join(s["text"] for s in samples["human_formal"])
    t0 = time.perf_counter()
    try:
        detector.model_signal(text)
    except Exception as exc:  # noqa: BLE001
        worker.log.warning("Model warm-up failed, first /submit will be slow or 503: %s", exc)
        return
    worker.log.info("Model warmed up in %.1f s", time.perf_counter() - t0)
