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
