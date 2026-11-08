"""
gunicorn settings (unit 9)

    gunicorn app:app            # finds this file on its own

pretty much everything in here is because of the model, not traffic
"""

import os

# same HOST/PORT as python app.py so the curl commands still work
bind = f"{os.getenv('HOST', '127.0.0.1')}:{os.getenv('PORT', '5000')}"

# only 1 worker. each worker loads its own gpt2 (~1.1gb, see readme) and the
# rate limiter counts are in memory per process, so 2 workers = double the ram
# AND everyone gets double the rate limit
workers = 1
threads = 1

# loading gpt2 can take a while on a slow laptop and the default 30s timeout
# could kill the worker mid load, so 2 min
timeout = 120

# no access log, requestlog.py already does that (logs/requests.jsonl).
# errors/tracebacks still show up in the terminal
accesslog = None
errorlog = "-"
loglevel = "info"


def post_worker_init(worker):
    """
    the unit 9 fix: warm up the model before the worker takes requests.

    before this the first /submit after every restart had to load gpt2 AND do
    torch's slow first forward pass (~3.5s + ~3.7s when i timed it), while
    /health was already saying ok. just loading isnt enough, so this actually
    scores a passage long enough to fill the 400 token window.

    gunicorn is already listening while this runs so early requests just wait
    in the queue. if the model cant load the worker starts anyway and /submit
    gives a 503 like before.
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
