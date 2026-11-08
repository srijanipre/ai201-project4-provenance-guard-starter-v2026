# Unit 9 clean-checkout check, 2026-11-08

Fresh git clone of the repo at e069591 into a temp folder, a new python3.13 venv,
then RUNNING.md's Unit 9 steps 1, 3 and 4 run as written. Step 2 (the model download)
was skipped because gpt2 was already in ~/.cache/huggingface, which test.py reports.
Temp paths are shortened to <tmp>.

## Steps 1: clone, venv, pip install, test.py

```
Sun Nov  8 14:32:09 CST 2026
e069591 Test the request log and keep route tests out of logs/
Python 3.13.15

[notice] A new release of pip is available: 26.2 -> 26.3
[notice] To update, run: pip install --upgrade pip
real 55.70
user 16.84
sys 6.00
Flask              3.1.3
Flask-Limiter      3.12
gunicorn           23.0.0
torch              2.15.0
transformers       4.57.6

AI201 environment check
------------------------------------------------------------
[PASS] Python version
         3.13.15 on Darwin
[PASS] Virtual environment
         <tmp>/clean/repo/.venv
[PASS] Pinned packages
         all 7 import cleanly
[FAIL] Free disk space
         1.5 GB free, need about 9 GB. PyTorch and the detector model cache are most of it.
[PASS] Memory
         8.0 GB
[PASS] PyTorch
         2.15.0
[PASS] Flask
         flask and flask-limiter both import
[PASS] Detector model
         already downloaded
[PASS] The service
         /ping answers — the starter works before you edit it
------------------------------------------------------------
8 passed, 1 failed, 0 to look at, 0 skipped

Not ready yet. Fix the FAIL lines above, then run test.py again.
Still stuck after one honest attempt? Post the whole output in the
help channel — the day before class, not the morning of.

real 12.10
user 1.33
sys 0.28
EXIT 1
Sun Nov  8 14:33:19 CST 2026
```

The one FAIL is free disk space on this laptop (the fresh venv's torch install
took it to 1.5 GB free). Everything the service needs passed.

## Steps 3 and 4: gunicorn, /health, /submit, request log

```
--- health
{"detector_loaded":false,"detector_model":"gpt2","log_entries":597,"ok":true,"rate_limiting":true}
--- submit
{"confidence":0.7641,"content_id":"ea7373ca-f70b-49ff-8c05-1b3ab8dae25c","guess":"ai","label":"Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.","model_score":0.716,"status":"decided","style_score":0.8363}

HTTP 200 in 9.814381s
--- requestlog
{"timestamp": "2026-11-08T20:33:29.780+00:00", "method": "GET", "path": "/health", "status": 200, "duration_ms": 2.1, "in_bytes": 0, "in_text_chars": null, "creator_id": null, "out_bytes": 99, "content_id": null, "guess": null, "confidence": null, "error": null, "exception": null, "model_loaded": false}
{"timestamp": "2026-11-08T20:33:29.796+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 9808.8, "in_bytes": 99, "in_text_chars": 67, "creator_id": "me", "out_bytes": 339, "content_id": "ea7373ca-f70b-49ff-8c05-1b3ab8dae25c", "guess": "ai", "confidence": 0.7641, "error": null, "exception": null, "model_loaded": false}
--- gunicorn output
[2026-11-08 14:33:29 -0600] [26338] [INFO] Starting gunicorn 23.0.0
[2026-11-08 14:33:29 -0600] [26338] [INFO] Listening at: http://127.0.0.1:5050 (26338)
[2026-11-08 14:33:29 -0600] [26338] [INFO] Using worker: sync
[2026-11-08 14:33:29 -0600] [26343] [INFO] Booting worker with pid: 26343
`loss_type=None` was set in the config but it is unrecognized. Using the default loss: `ForCausalLMLoss`.
[2026-11-08 14:33:39 -0600] [26343] [INFO] Worker exiting (pid: 26343)
[2026-11-08 14:33:39 -0600] [26338] [INFO] Handling signal: term
[2026-11-08 14:33:40 -0600] [26338] [INFO] Shutting down: Master
```
