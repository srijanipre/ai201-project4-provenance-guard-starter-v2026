#!/usr/bin/env python3
"""
Measure what one request costs to run. UNIT 9, MILESTONE 3.

There's no paid API here, so the cost is compute: seconds of server time per
/submit. This starts the service under gunicorn itself, so every cold start is
a real fresh process.

    python measure_cost.py                 # 3 cold starts, then 10 warm requests
    python measure_cost.py --cold 3 --warm 10 --port 5050

Two numbers per request:
  - duration_ms: the server's own timing, read back from the request log
    (requestlog.py). Starts before the rate limiter, ends after the response
    is built.
  - client_ms: the round trip measured here, around requests.post.

Writes results/cost_<date>.md. The request-log lines it reads are the real
ones in logs/requests.jsonl (or AI201_REQUEST_LOG, if set).
"""

import argparse
import datetime as dt
import json
import os
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import requests

import config

ROOT = Path(__file__).resolve().parent

# 303 words: two formal calibration passages joined. That's 365 gpt2 tokens,
# close to the 400-token window (config.DETECTOR_MAX_TOKENS), so it's near the
# most expensive ordinary submission. Shorter text is cheaper.
_CAL = json.loads((ROOT / "samples" / "calibration.json").read_text(encoding="utf-8"))
COST_TEXT = _CAL["human_formal"][3]["text"] + " " + _CAL["human_formal"][4]["text"]


# ── Starting and stopping a real server ──────────────────────────────────────

def start_server(port: int, env_extra: dict | None = None, timeout: float = 180.0):
    """
    Start `gunicorn app:app` on `port` and wait until /health answers.

    Returns (process, seconds from launch until /health first answered).
    gunicorn's own output goes to a temp file, so a full pipe can never stall it.
    """
    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", **(env_extra or {}))
    errfile = tempfile.TemporaryFile(mode="w+")
    t0 = time.perf_counter()
    proc = subprocess.Popen(
        [sys.executable, "-m", "gunicorn", "app:app"],
        cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=errfile, text=True,
    )
    url = f"http://127.0.0.1:{port}/health"
    while time.perf_counter() - t0 < timeout:
        if proc.poll() is not None:
            errfile.seek(0)
            raise RuntimeError(f"gunicorn exited early:\n{errfile.read()}")
        try:
            # A long read timeout: if the worker is busy (say, loading the
            # model) the connection waits in the queue, and that wait is part
            # of what's being measured.
            if requests.get(url, timeout=(1, 120)).status_code == 200:
                return proc, time.perf_counter() - t0
        except requests.RequestException:
            pass
        time.sleep(0.05)
    proc.terminate()
    raise RuntimeError(f"gunicorn didn't answer on port {port} within {timeout}s")


def stop_server(proc) -> None:
    proc.terminate()
    try:
        proc.wait(timeout=15)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()


def worker_pid(master_pid: int) -> int | None:
    out = subprocess.run(["pgrep", "-P", str(master_pid)], capture_output=True, text=True).stdout.split()
    return int(out[0]) if out else None


def rss_mb(pid: int) -> float:
    kb = subprocess.run(["ps", "-o", "rss=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    return round(int(kb) / 1024, 1)


def cpu_seconds(pid: int) -> float:
    """Total CPU time (all threads) a process has used, from `ps -o time=`."""
    raw = subprocess.run(["ps", "-o", "time=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    parts = [float(p) for p in raw.split(":")]
    secs = 0.0
    for p in parts:
        secs = secs * 60 + p
    return secs


# ── Reading the request log ──────────────────────────────────────────────────

def log_size() -> int:
    return config.REQUEST_LOG.stat().st_size if config.REQUEST_LOG.exists() else 0


def log_lines_since(offset: int) -> list[dict]:
    if not config.REQUEST_LOG.exists():
        return []
    with config.REQUEST_LOG.open("rb") as f:
        f.seek(offset)
        raw = f.read().decode("utf-8")
    return [json.loads(x) for x in raw.splitlines() if x.strip()]


def timed_submit(base: str, creator: str, text: str = COST_TEXT) -> dict:
    t0 = time.perf_counter()
    r = requests.post(f"{base}/submit", json={"text": text, "creator_id": creator}, timeout=180)
    client_ms = round((time.perf_counter() - t0) * 1000, 1)
    return {"status": r.status_code, "client_ms": client_ms, "body": r.json()}


def submit_line(lines: list[dict], content_id: str) -> dict:
    return next(e for e in lines if e["path"] == "/submit" and e["content_id"] == content_id)


# ── The measurement ──────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cold", type=int, default=3)
    ap.add_argument("--warm", type=int, default=10)
    ap.add_argument("--port", type=int, default=5050)
    args = ap.parse_args()
    base = f"http://127.0.0.1:{args.port}"
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")

    cold = []
    for i in range(1, args.cold + 1):
        offset = log_size()
        proc, ready_s = start_server(args.port)
        try:
            res = timed_submit(base, f"cost_cold_{stamp}_{i}")
            line = submit_line(log_lines_since(offset), res["body"]["content_id"])
        finally:
            stop_server(proc)
        cold.append({"trial": i, "ready_s": round(ready_s, 2), "client_ms": res["client_ms"],
                     "duration_ms": line["duration_ms"], "model_loaded": line["model_loaded"],
                     "log_line": line})
        print(f"cold {i}: ready {ready_s:.2f}s, first submit {line['duration_ms']} ms "
              f"(client {res['client_ms']} ms, model_loaded={line['model_loaded']})")

    proc, ready_s = start_server(args.port)
    try:
        wpid = worker_pid(proc.pid)
        rss_idle = rss_mb(wpid)
        timed_submit(base, f"cost_warmup_{stamp}")          # loads the model; not counted
        rss_loaded = rss_mb(wpid)
        offset = log_size()
        cpu0 = cpu_seconds(wpid)
        warm = []
        for i in range(1, args.warm + 1):
            res = timed_submit(base, f"cost_warm_{stamp}_{i}")
            warm.append(res)
        cpu1 = cpu_seconds(wpid)
        lines = log_lines_since(offset)
        rss_after = rss_mb(wpid)
    finally:
        stop_server(proc)

    rows = []
    for i, res in enumerate(warm, 1):
        line = submit_line(lines, res["body"]["content_id"])
        rows.append({"run": i, "status": res["status"], "client_ms": res["client_ms"],
                     "duration_ms": line["duration_ms"], "model_loaded": line["model_loaded"],
                     "log_line": line})
        print(f"warm {i}: {line['duration_ms']} ms (client {res['client_ms']} ms)")

    durs = [r["duration_ms"] for r in rows]
    summary = {
        "text_words": len(COST_TEXT.split()),
        "cold_mean_first_submit_ms": round(statistics.mean(c["duration_ms"] for c in cold), 1) if cold else None,
        "cold_mean_ready_s": round(statistics.mean(c["ready_s"] for c in cold), 2) if cold else None,
        "warm_mean_ms": round(statistics.mean(durs), 1),
        "warm_median_ms": round(statistics.median(durs), 1),
        "warm_min_ms": min(durs),
        "warm_max_ms": max(durs),
        "warm_mean_client_ms": round(statistics.mean(r["client_ms"] for r in rows), 1),
        "worker_cpu_s_per_request": round((cpu1 - cpu0) / len(rows), 3),
        "worker_rss_mb_before_model": rss_idle,
        "worker_rss_mb_after_model": rss_loaded,
        "worker_rss_mb_after_warm_runs": rss_after,
    }
    print(json.dumps(summary, indent=2))

    config.RESULTS_DIR.mkdir(exist_ok=True)
    path = config.RESULTS_DIR / f"cost_{stamp}.md"
    out = [f"# Cost measurement, {stamp}", "",
           "- Produced by: `measure_cost.py::main`, server `gunicorn app:app` (gunicorn.conf.py)",
           f"- Text: {summary['text_words']} words (365 gpt2 tokens; the window is 400)",
           "- duration_ms is the server's own timing from the request log; client_ms is the round trip", "",
           "## Summary", "", "```json", json.dumps(summary, indent=2), "```", "",
           "## Cold starts (fresh gunicorn each)", "",
           "| Trial | Launch to /health (s) | First /submit duration_ms | client_ms | model_loaded |",
           "|---|---|---|---|---|"]
    out += [f"| {c['trial']} | {c['ready_s']} | {c['duration_ms']} | {c['client_ms']} | {c['model_loaded']} |"
            for c in cold]
    out += ["", "## Warm requests (one server, after one uncounted warm-up)", "",
            "| Run | Status | duration_ms | client_ms |", "|---|---|---|---|"]
    out += [f"| {r['run']} | {r['status']} | {r['duration_ms']} | {r['client_ms']} |" for r in rows]
    out += ["", "## Request-log lines", "", "```json"]
    out += [json.dumps(c["log_line"]) for c in cold] + [json.dumps(r["log_line"]) for r in rows]
    out += ["```", ""]
    path.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
