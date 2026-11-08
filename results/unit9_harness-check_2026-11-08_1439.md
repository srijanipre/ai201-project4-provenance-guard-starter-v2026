# Unit 9 criteria, harness-check

- Produced by: `run_ops_eval.py::main`; each trial is a fresh `gunicorn app:app` on port 5050
- Request log for this run: `logs/requests_unit9_harness-check.jsonl`
- 1 trials per criterion, 2026-11-08 14:39

| Criterion | Target | Trial 1 | Verdict |
|---|---|---|---|
| U9-1. Every request leaves one complete log line | 20 lines, 20/20 complete and matching, 0 text leaks | 20 lines, 20/20 complete, 0 leaks (held) | MET |
| U9-2. Every refused request says why | 22/22 status and error match, 0 5xx, 429 logged | 22/22 match, 0 5xx, 429 logged: True (held) | MET |
| U9-3. Warm requests cheap, logged time honest | mean ≤ 300 ms, max ≤ 500 ms, each within 15 ms of client | mean 214.7 ms, max 238.4 ms, max gap 4.9 ms (held) | MET |
| U9-4. First request after a start isn't cold | first /submit ≤ 1.0 s after /health answers | first submit 3141.7 ms (ready after 0.19 s) (missed) | MISSED |
| U9-5. Unit 8 behaviour unchanged under gunicorn | c1/3/4/5 held, gap 0.201, audit shapes, all tests pass | c1/3/4/5 held: [True, True, True, True], gap 0.201, 62/62 audit lines right shape, tests OK (33) (held) | MET |

## Every trial, as measured

### U9-1. Every request leaves one complete log line

Check: `run_ops_eval.py::criterion_1`

**Trial 1**

```json
{
  "value": "20 lines, 20/20 complete, 0 leaks",
  "passed": true,
  "requests_sent": 20,
  "lines_added": 20,
  "complete_and_matching": 20,
  "text_leaks": 0,
  "client_statuses": [
    200,
    200,
    200,
    200,
    200,
    200,
    200,
    200,
    200,
    200,
    200,
    200,
    200,
    409,
    404,
    200,
    200,
    400,
    404,
    200
  ],
  "log_statuses": [
    200,
    200,
    200,
    200,
    200,
    200,
    200,
    200,
    200,
    200,
    200,
    200,
    200,
    409,
    404,
    200,
    200,
    400,
    404,
    200
  ],
  "trial": 1
}
```

Request-log lines this check read:

```json
{"timestamp": "2026-11-08T20:38:30.274+00:00", "method": "POST", "path": "/ping", "status": 200, "duration_ms": 0.1, "in_bytes": 20, "in_text_chars": null, "creator_id": null, "out_bytes": 60, "content_id": null, "guess": null, "confidence": null, "error": null, "exception": null, "model_loaded": false}
{"timestamp": "2026-11-08T20:38:30.276+00:00", "method": "GET", "path": "/health", "status": 200, "duration_ms": 1.5, "in_bytes": 0, "in_text_chars": null, "creator_id": null, "out_bytes": 99, "content_id": null, "guess": null, "confidence": null, "error": null, "exception": null, "model_loaded": false}
{"timestamp": "2026-11-08T20:38:30.279+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 7819.2, "in_bytes": 630, "in_text_chars": 552, "creator_id": "u9c1_harness-check_t1_0", "out_bytes": 288, "content_id": "2e001f52-9d5b-448c-966b-7bbbd1b7b278", "guess": "human", "confidence": 0.2985, "error": null, "exception": null, "model_loaded": false}
{"timestamp": "2026-11-08T20:38:38.113+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 150.2, "in_bytes": 358, "in_text_chars": 295, "creator_id": "u9c1_harness-check_t1_1", "out_bytes": 348, "content_id": "c0adb57a-037a-457a-a4c8-d02f8e715f50", "guess": "unsure", "confidence": 0.4773, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:38.266+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 147.9, "in_bytes": 610, "in_text_chars": 542, "creator_id": "u9c1_harness-check_t1_2", "out_bytes": 348, "content_id": "f2c689ff-1362-4de8-a1ac-44043229161a", "guess": "unsure", "confidence": 0.4223, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:38.417+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 119.6, "in_bytes": 564, "in_text_chars": 496, "creator_id": "u9c1_harness-check_t1_3", "out_bytes": 288, "content_id": "bba10f3c-bdd7-4764-acf4-fdae1cd47f39", "guess": "human", "confidence": 0.2653, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:38.540+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 145.8, "in_bytes": 487, "in_text_chars": 434, "creator_id": "u9c1_harness-check_t1_4", "out_bytes": 346, "content_id": "519295c1-435e-4cb3-9381-a68b23bd191e", "guess": "unsure", "confidence": 0.4394, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:38.689+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 234.3, "in_bytes": 887, "in_text_chars": 834, "creator_id": "u9c1_harness-check_t1_5", "out_bytes": 347, "content_id": "0015155b-0df1-4dbe-ae13-c739aa516213", "guess": "unsure", "confidence": 0.5772, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:38.933+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 274.5, "in_bytes": 675, "in_text_chars": 622, "creator_id": "u9c1_harness-check_t1_6", "out_bytes": 347, "content_id": "f00b5b0d-d62e-4122-aabe-4b0b60d2ce4a", "guess": "unsure", "confidence": 0.618, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:39.213+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 119.3, "in_bytes": 659, "in_text_chars": 606, "creator_id": "u9c1_harness-check_t1_7", "out_bytes": 348, "content_id": "1450a9a4-8e64-43d9-9aeb-14cb606f2af6", "guess": "unsure", "confidence": 0.5768, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:39.335+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 159.5, "in_bytes": 906, "in_text_chars": 843, "creator_id": "u9c1_harness-check_t1_8", "out_bytes": 347, "content_id": "cefb5094-20c4-4e25-9184-bcd09c83f97b", "guess": "unsure", "confidence": 0.5666, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:39.497+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 171.1, "in_bytes": 981, "in_text_chars": 918, "creator_id": "u9c1_harness-check_t1_9", "out_bytes": 348, "content_id": "519a68b4-5d2e-480b-a5ea-5ccc7b55ea6c", "guess": "unsure", "confidence": 0.3908, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:39.671+00:00", "method": "POST", "path": "/appeal", "status": 200, "duration_ms": 5.3, "in_bytes": 84, "in_text_chars": null, "creator_id": null, "out_bytes": 364, "content_id": "2e001f52-9d5b-448c-966b-7bbbd1b7b278", "guess": null, "confidence": null, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:39.688+00:00", "method": "POST", "path": "/appeal", "status": 409, "duration_ms": 4.2, "in_bytes": 77, "in_text_chars": null, "creator_id": null, "out_bytes": 92, "content_id": "2e001f52-9d5b-448c-966b-7bbbd1b7b278", "guess": null, "confidence": null, "error": "already_under_review", "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:39.716+00:00", "method": "POST", "path": "/appeal", "status": 404, "duration_ms": 7.3, "in_bytes": 53, "in_text_chars": null, "creator_id": null, "out_bytes": 86, "content_id": "no-such-id", "guess": null, "confidence": null, "error": "content_not_found", "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:39.727+00:00", "method": "GET", "path": "/log", "status": 200, "duration_ms": 9.8, "in_bytes": 0, "in_text_chars": null, "creator_id": null, "out_bytes": 2167, "content_id": null, "guess": null, "confidence": null, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:39.742+00:00", "method": "GET", "path": "/log", "status": 200, "duration_ms": 2.8, "in_bytes": 0, "in_text_chars": null, "creator_id": null, "out_bytes": 445, "content_id": null, "guess": null, "confidence": null, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:39.747+00:00", "method": "POST", "path": "/submit", "status": 400, "duration_ms": 0.5, "in_bytes": 18, "in_text_chars": null, "creator_id": null, "out_bytes": 86, "content_id": null, "guess": null, "confidence": null, "error": "invalid_body", "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:39.749+00:00", "method": "GET", "path": "/no-such-route", "status": 404, "duration_ms": 0.8, "in_bytes": 0, "in_text_chars": null, "creator_id": null, "out_bytes": 207, "content_id": null, "guess": null, "confidence": null, "error": "http_404", "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:39.753+00:00", "method": "GET", "path": "/health", "status": 200, "duration_ms": 1.8, "in_bytes": 0, "in_text_chars": null, "creator_id": null, "out_bytes": 98, "content_id": null, "guess": null, "confidence": null, "error": null, "exception": null, "model_loaded": true}
```

### U9-2. Every refused request says why

Check: `run_ops_eval.py::criterion_2`

**Trial 1**

```json
{
  "value": "22/22 match, 0 5xx, 429 logged: True",
  "passed": true,
  "lines_added": 22,
  "flood_statuses": [
    400,
    400,
    400,
    400,
    400,
    400,
    400,
    400,
    400,
    400,
    429
  ],
  "rows": [
    {
      "path": "/submit",
      "client_status": 400,
      "client_error": "empty_text",
      "log_status": 400,
      "log_error": "empty_text",
      "ok": true
    },
    {
      "path": "/submit",
      "client_status": 400,
      "client_error": "empty_text",
      "log_status": 400,
      "log_error": "empty_text",
      "ok": true
    },
    {
      "path": "/submit",
      "client_status": 400,
      "client_error": "missing_field",
      "log_status": 400,
      "log_error": "missing_field",
      "ok": true
    },
    {
      "path": "/submit",
      "client_status": 400,
      "client_error": "invalid_type",
      "log_status": 400,
      "log_error": "invalid_type",
      "ok": true
    },
    {
      "path": "/submit",
      "client_status": 400,
      "client_error": "invalid_type",
      "log_status": 400,
      "log_error": "invalid_type",
      "ok": true
    },
    {
      "path": "/submit",
      "client_status": 400,
      "client_error": "missing_field",
      "log_status": 400,
      "log_error": "missing_field",
      "ok": true
    },
    {
      "path": "/submit",
      "client_status": 413,
      "client_error": "text_too_long",
      "log_status": 413,
      "log_error": "text_too_long",
      "ok": true
    },
    {
      "path": "/submit",
      "client_status": 400,
      "client_error": "invalid_body",
      "log_status": 400,
      "log_error": "invalid_body",
      "ok": true
    },
    {
      "path": "/submit",
      "client_status": 422,
      "client_error": "text_too_short",
      "log_status": 422,
      "log_error": "text_too_short",
      "ok": true
    },
    {
      "path": "/appeal",
      "client_status": 404,
      "client_error": "content_not_found",
      "log_status": 404,
      "log_error": "content_not_found",
      "ok": true
    },
    {
      "path": "/no-such-route",
      "client_status": 404,
      "client_error": "http_404",
      "log_status": 404,
      "log_error": "http_404",
      "ok": true
    },
    {
      "path": "/submit",
      "client_status": 400,
      "client_error": "empty_text",
      "log_status": 400,
      "log_error": "empty_text",
      "ok": true
    },
    {
      "path": "/submit",
      "client_status": 400,
      "client_error": "empty_text",
      "log_status": 400,
      "log_error": "empty_text",
      "ok": true
    },
    {
      "path": "/submit",
      "client_status": 400,
      "client_error": "empty_text",
      "log_status": 400,
      "log_error": "empty_text",
      "ok": true
    },
    {
      "path": "/submit",
      "client_status": 400,
      "client_error": "empty_text",
      "log_status": 400,
      "log_error": "empty_text",
      "ok": true
    },
    {
      "path": "/submit",
      "client_status": 400,
      "client_error": "empty_text",
      "log_status": 400,
      "log_error": "empty_text",
      "ok": true
    },
    {
      "path": "/submit",
      "client_status": 400,
      "client_error": "empty_text",
      "log_status": 400,
      "log_error": "empty_text",
      "ok": true
    },
    {
      "path": "/submit",
      "client_status": 400,
      "client_error": "empty_text",
      "log_status": 400,
      "log_error": "empty_text",
      "ok": true
    },
    {
      "path": "/submit",
      "client_status": 400,
      "client_error": "empty_text",
      "log_status": 400,
      "log_error": "empty_text",
      "ok": true
    },
    {
      "path": "/submit",
      "client_status": 400,
      "client_error": "empty_text",
      "log_status": 400,
      "log_error": "empty_text",
      "ok": true
    },
    {
      "path": "/submit",
      "client_status": 400,
      "client_error": "empty_text",
      "log_status": 400,
      "log_error": "empty_text",
      "ok": true
    },
    {
      "path": "/submit",
      "client_status": 429,
      "client_error": "rate_limited",
      "log_status": 429,
      "log_error": "rate_limited",
      "ok": true
    }
  ],
  "trial": 1
}
```

Request-log lines this check read:

```json
{"timestamp": "2026-11-08T20:38:42.310+00:00", "method": "POST", "path": "/submit", "status": 400, "duration_ms": 0.4, "in_bytes": 44, "in_text_chars": 0, "creator_id": "eval_bad_empty", "out_bytes": 71, "content_id": null, "guess": null, "confidence": null, "error": "empty_text", "exception": null, "model_loaded": false}
{"timestamp": "2026-11-08T20:38:42.312+00:00", "method": "POST", "path": "/submit", "status": 400, "duration_ms": 0.2, "in_bytes": 52, "in_text_chars": 6, "creator_id": "eval_bad_space", "out_bytes": 71, "content_id": null, "guess": null, "confidence": null, "error": "empty_text", "exception": null, "model_loaded": false}
{"timestamp": "2026-11-08T20:38:42.314+00:00", "method": "POST", "path": "/submit", "status": 400, "duration_ms": 0.2, "in_bytes": 34, "in_text_chars": null, "creator_id": "eval_bad_missing", "out_bytes": 58, "content_id": null, "guess": null, "confidence": null, "error": "missing_field", "exception": null, "model_loaded": false}
{"timestamp": "2026-11-08T20:38:42.315+00:00", "method": "POST", "path": "/submit", "status": 400, "duration_ms": 0.2, "in_bytes": 45, "in_text_chars": null, "creator_id": "eval_bad_null", "out_bytes": 62, "content_id": null, "guess": null, "confidence": null, "error": "invalid_type", "exception": null, "model_loaded": false}
{"timestamp": "2026-11-08T20:38:42.316+00:00", "method": "POST", "path": "/submit", "status": 400, "duration_ms": 0.2, "in_bytes": 48, "in_text_chars": null, "creator_id": "eval_bad_number", "out_bytes": 62, "content_id": null, "guess": null, "confidence": null, "error": "invalid_type", "exception": null, "model_loaded": false}
{"timestamp": "2026-11-08T20:38:42.318+00:00", "method": "POST", "path": "/submit", "status": 400, "duration_ms": 0.2, "in_bytes": 73, "in_text_chars": 61, "creator_id": null, "out_bytes": 64, "content_id": null, "guess": null, "confidence": null, "error": "missing_field", "exception": null, "model_loaded": false}
{"timestamp": "2026-11-08T20:38:42.319+00:00", "method": "POST", "path": "/submit", "status": 413, "duration_ms": 0.2, "in_bytes": 12543, "in_text_chars": 12500, "creator_id": "eval_bad_huge", "out_bytes": 86, "content_id": null, "guess": null, "confidence": null, "error": "text_too_long", "exception": null, "model_loaded": false}
{"timestamp": "2026-11-08T20:38:42.320+00:00", "method": "POST", "path": "/submit", "status": 400, "duration_ms": 0.2, "in_bytes": 18, "in_text_chars": null, "creator_id": null, "out_bytes": 86, "content_id": null, "guess": null, "confidence": null, "error": "invalid_body", "exception": null, "model_loaded": false}
{"timestamp": "2026-11-08T20:38:42.321+00:00", "method": "POST", "path": "/submit", "status": 422, "duration_ms": 3667.4, "in_bytes": 59, "in_text_chars": 2, "creator_id": "u9c2_harness-check_t1_short", "out_bytes": 99, "content_id": null, "guess": null, "confidence": null, "error": "text_too_short", "exception": null, "model_loaded": false}
{"timestamp": "2026-11-08T20:38:45.993+00:00", "method": "POST", "path": "/appeal", "status": 404, "duration_ms": 4.1, "in_bytes": 53, "in_text_chars": null, "creator_id": null, "out_bytes": 86, "content_id": "no-such-id", "guess": null, "confidence": null, "error": "content_not_found", "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:45.999+00:00", "method": "GET", "path": "/no-such-route", "status": 404, "duration_ms": 0.2, "in_bytes": 0, "in_text_chars": null, "creator_id": null, "out_bytes": 207, "content_id": null, "guess": null, "confidence": null, "error": "http_404", "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:46.002+00:00", "method": "POST", "path": "/submit", "status": 400, "duration_ms": 0.4, "in_bytes": 57, "in_text_chars": 0, "creator_id": "u9c2_harness-check_t1_flood", "out_bytes": 71, "content_id": null, "guess": null, "confidence": null, "error": "empty_text", "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:46.004+00:00", "method": "POST", "path": "/submit", "status": 400, "duration_ms": 0.3, "in_bytes": 57, "in_text_chars": 0, "creator_id": "u9c2_harness-check_t1_flood", "out_bytes": 71, "content_id": null, "guess": null, "confidence": null, "error": "empty_text", "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:46.006+00:00", "method": "POST", "path": "/submit", "status": 400, "duration_ms": 0.2, "in_bytes": 57, "in_text_chars": 0, "creator_id": "u9c2_harness-check_t1_flood", "out_bytes": 71, "content_id": null, "guess": null, "confidence": null, "error": "empty_text", "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:46.007+00:00", "method": "POST", "path": "/submit", "status": 400, "duration_ms": 0.2, "in_bytes": 57, "in_text_chars": 0, "creator_id": "u9c2_harness-check_t1_flood", "out_bytes": 71, "content_id": null, "guess": null, "confidence": null, "error": "empty_text", "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:46.009+00:00", "method": "POST", "path": "/submit", "status": 400, "duration_ms": 0.2, "in_bytes": 57, "in_text_chars": 0, "creator_id": "u9c2_harness-check_t1_flood", "out_bytes": 71, "content_id": null, "guess": null, "confidence": null, "error": "empty_text", "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:46.011+00:00", "method": "POST", "path": "/submit", "status": 400, "duration_ms": 0.3, "in_bytes": 57, "in_text_chars": 0, "creator_id": "u9c2_harness-check_t1_flood", "out_bytes": 71, "content_id": null, "guess": null, "confidence": null, "error": "empty_text", "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:46.013+00:00", "method": "POST", "path": "/submit", "status": 400, "duration_ms": 0.2, "in_bytes": 57, "in_text_chars": 0, "creator_id": "u9c2_harness-check_t1_flood", "out_bytes": 71, "content_id": null, "guess": null, "confidence": null, "error": "empty_text", "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:46.015+00:00", "method": "POST", "path": "/submit", "status": 400, "duration_ms": 0.3, "in_bytes": 57, "in_text_chars": 0, "creator_id": "u9c2_harness-check_t1_flood", "out_bytes": 71, "content_id": null, "guess": null, "confidence": null, "error": "empty_text", "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:46.017+00:00", "method": "POST", "path": "/submit", "status": 400, "duration_ms": 0.2, "in_bytes": 57, "in_text_chars": 0, "creator_id": "u9c2_harness-check_t1_flood", "out_bytes": 71, "content_id": null, "guess": null, "confidence": null, "error": "empty_text", "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:46.019+00:00", "method": "POST", "path": "/submit", "status": 400, "duration_ms": 0.2, "in_bytes": 57, "in_text_chars": 0, "creator_id": "u9c2_harness-check_t1_flood", "out_bytes": 71, "content_id": null, "guess": null, "confidence": null, "error": "empty_text", "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:46.020+00:00", "method": "POST", "path": "/submit", "status": 429, "duration_ms": 0.2, "in_bytes": 57, "in_text_chars": 0, "creator_id": "u9c2_harness-check_t1_flood", "out_bytes": 104, "content_id": null, "guess": null, "confidence": null, "error": "rate_limited", "exception": null, "model_loaded": true}
```

### U9-3. Warm requests cheap, logged time honest

Check: `run_ops_eval.py::criterion_3`

**Trial 1**

```json
{
  "value": "mean 214.7 ms, max 238.4 ms, max gap 4.9 ms",
  "passed": true,
  "mean_ms": 214.7,
  "max_ms": 238.4,
  "max_gap_ms": 4.9,
  "runs": [
    {
      "status": 200,
      "duration_ms": 238.4,
      "client_ms": 243.3,
      "gap_ms": 4.9
    },
    {
      "status": 200,
      "duration_ms": 211.6,
      "client_ms": 213.9,
      "gap_ms": 2.3
    },
    {
      "status": 200,
      "duration_ms": 211.5,
      "client_ms": 213.8,
      "gap_ms": 2.3
    },
    {
      "status": 200,
      "duration_ms": 207.1,
      "client_ms": 209.6,
      "gap_ms": 2.5
    },
    {
      "status": 200,
      "duration_ms": 210.5,
      "client_ms": 212.9,
      "gap_ms": 2.4
    },
    {
      "status": 200,
      "duration_ms": 212.3,
      "client_ms": 214.5,
      "gap_ms": 2.2
    },
    {
      "status": 200,
      "duration_ms": 208.2,
      "client_ms": 210.4,
      "gap_ms": 2.2
    },
    {
      "status": 200,
      "duration_ms": 213.7,
      "client_ms": 216.0,
      "gap_ms": 2.3
    },
    {
      "status": 200,
      "duration_ms": 217.1,
      "client_ms": 219.5,
      "gap_ms": 2.4
    },
    {
      "status": 200,
      "duration_ms": 217.0,
      "client_ms": 219.4,
      "gap_ms": 2.4
    }
  ],
  "trial": 1
}
```

Request-log lines this check read:

```json
{"timestamp": "2026-11-08T20:38:53.281+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 238.4, "in_bytes": 1835, "in_text_chars": 1762, "creator_id": "u9c3_harness-check_t1_0", "out_bytes": 347, "content_id": "8594d187-af8b-415a-a61f-cfab0fcebedc", "guess": "unsure", "confidence": 0.4236, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:53.522+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 211.6, "in_bytes": 1835, "in_text_chars": 1762, "creator_id": "u9c3_harness-check_t1_1", "out_bytes": 347, "content_id": "311e1c7f-13ac-4ed2-bf29-8c15c291236e", "guess": "unsure", "confidence": 0.4236, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:53.736+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 211.5, "in_bytes": 1835, "in_text_chars": 1762, "creator_id": "u9c3_harness-check_t1_2", "out_bytes": 347, "content_id": "84b18783-752c-4ca3-b213-4d163fa662ac", "guess": "unsure", "confidence": 0.4236, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:53.950+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 207.1, "in_bytes": 1835, "in_text_chars": 1762, "creator_id": "u9c3_harness-check_t1_3", "out_bytes": 347, "content_id": "2686b000-db95-4ce0-b779-8b1b579a288e", "guess": "unsure", "confidence": 0.4236, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:54.159+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 210.5, "in_bytes": 1835, "in_text_chars": 1762, "creator_id": "u9c3_harness-check_t1_4", "out_bytes": 347, "content_id": "d7fae851-a6da-44ca-8c23-d1bd9a34bb78", "guess": "unsure", "confidence": 0.4236, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:54.372+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 212.3, "in_bytes": 1835, "in_text_chars": 1762, "creator_id": "u9c3_harness-check_t1_5", "out_bytes": 347, "content_id": "90e25c20-ba7d-4edd-9d58-4f25c7aa07bd", "guess": "unsure", "confidence": 0.4236, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:54.587+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 208.2, "in_bytes": 1835, "in_text_chars": 1762, "creator_id": "u9c3_harness-check_t1_6", "out_bytes": 347, "content_id": "d49d9b23-997a-46a8-9368-9841be69de47", "guess": "unsure", "confidence": 0.4236, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:54.797+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 213.7, "in_bytes": 1835, "in_text_chars": 1762, "creator_id": "u9c3_harness-check_t1_7", "out_bytes": 347, "content_id": "e94999fe-3c0f-4ff9-8a48-b9543f452761", "guess": "unsure", "confidence": 0.4236, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:55.013+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 217.1, "in_bytes": 1835, "in_text_chars": 1762, "creator_id": "u9c3_harness-check_t1_8", "out_bytes": 347, "content_id": "1df93458-eede-4c0b-92fa-88afc5616caf", "guess": "unsure", "confidence": 0.4236, "error": null, "exception": null, "model_loaded": true}
{"timestamp": "2026-11-08T20:38:55.233+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 217.0, "in_bytes": 1835, "in_text_chars": 1762, "creator_id": "u9c3_harness-check_t1_9", "out_bytes": 347, "content_id": "88c70ad5-4312-452a-a1e7-669e31fdd37f", "guess": "unsure", "confidence": 0.4236, "error": null, "exception": null, "model_loaded": true}
```

### U9-4. First request after a start isn't cold

Check: `run_ops_eval.py::criterion_4`

**Trial 1**

```json
{
  "value": "first submit 3141.7 ms (ready after 0.19 s)",
  "passed": false,
  "launch_to_health_s": 0.19,
  "first_submit_client_ms": 3141.7,
  "first_submit_duration_ms": 3139.2,
  "model_loaded_at_first_submit": false,
  "trial": 1
}
```

Request-log lines this check read:

```json
{"timestamp": "2026-11-08T20:38:56.201+00:00", "method": "POST", "path": "/submit", "status": 200, "duration_ms": 3139.2, "in_bytes": 1833, "in_text_chars": 1762, "creator_id": "u9c4_harness-check_t1", "out_bytes": 347, "content_id": "0360ed7a-9b33-432e-9267-61670affc90b", "guess": "unsure", "confidence": 0.4236, "error": null, "exception": null, "model_loaded": false}
```

### U9-5. Unit 8 behaviour unchanged under gunicorn

Check: `run_ops_eval.py::criterion_5`

**Trial 1**

```json
{
  "value": "c1/3/4/5 held: [True, True, True, True], gap 0.201, 62/62 audit lines right shape, tests OK (33)",
  "passed": true,
  "run_eval_criteria": {
    "1": {
      "value": "0/10 AI",
      "held": true
    },
    "2": {
      "value": "gap 0.201",
      "held": false
    },
    "3": {
      "value": "3/3 labels, 6/6 bounds",
      "held": true
    },
    "4": {
      "value": "5/5 appeals, 3/3 errors",
      "held": true
    },
    "5": {
      "value": "8/8 clean, 0 decisions logged",
      "held": true
    }
  },
  "run_eval_results_file": "results/run_2026-11-08_1439_unit9_harness-check_t1.md",
  "audit_lines_added": 62,
  "audit_lines_wrong_shape": [],
  "unit_tests": [
    "Ran 33 tests in 6.322s",
    "",
    "OK"
  ],
  "request_log_lines_added": 88,
  "trial": 1
}
```
