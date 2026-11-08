#!/usr/bin/env python3
"""
Run the five Unit 9 criteria (criteria.md, "Unit 9 criteria") three times each.

    python run_ops_eval.py --label before
    python run_ops_eval.py --label before --only 4      # one criterion

Every trial starts its own fresh `gunicorn app:app` on --port (default 5050)
and stops it afterwards, so trials are independent: the rate limiter starts
empty and the model is never already loaded. The request log for a whole run
goes to logs/requests_unit9_<label>.jsonl; each trial reads only the lines it
added.

Writes results/unit9_<label>_<date>.md with the table, every trial's measured
values, and the request-log lines each check looked at.
"""

import argparse
import datetime as dt
import json
import re
import statistics
import subprocess
import sys
import time
from pathlib import Path

import requests

import config
import scenarios
from measure_cost import COST_TEXT, start_server, stop_server

ROOT = Path(__file__).resolve().parent

FIELDS = {"timestamp", "method", "path", "status", "duration_ms", "in_bytes",
          "in_text_chars", "creator_id", "out_bytes", "content_id", "guess",
          "confidence", "error", "exception", "model_loaded"}
NINE = {"timestamp", "content_id", "creator_id", "guess", "model_score",
        "style_score", "combined_score", "label", "status"}


class Server:
    """A fresh gunicorn for one trial, with a client that remembers what it got back."""

    def __init__(self, port: int, req_log: Path):
        self.port, self.req_log = port, req_log
        self.base = f"http://127.0.0.1:{port}"

    def __enter__(self):
        self.offset = self.req_log.stat().st_size if self.req_log.exists() else 0
        self.proc, self.ready_s = start_server(self.port, {"AI201_REQUEST_LOG": str(self.req_log)})
        # start_server's /health poll leaves one line; checks only count what
        # the trial itself sends, so skip past it.
        self.offset = self.req_log.stat().st_size
        return self

    def __exit__(self, *exc):
        stop_server(self.proc)

    def send(self, method: str, path: str, json_body=None, raw: str | None = None) -> dict:
        t0 = time.perf_counter()
        if raw is not None:
            r = requests.request(method, self.base + path, data=raw.encode(),
                                 headers={"Content-Type": "application/json"}, timeout=180)
        else:
            r = requests.request(method, self.base + path, json=json_body, timeout=180)
        client_ms = round((time.perf_counter() - t0) * 1000, 1)
        try:
            body = r.json()
        except ValueError:
            body = None
        return {"method": method, "path": path, "status": r.status_code, "client_ms": client_ms,
                "body": body if isinstance(body, dict) else {}}

    def new_lines(self) -> list[dict]:
        with self.req_log.open("rb") as f:
            f.seek(self.offset)
            raw = f.read().decode("utf-8")
        return [json.loads(x) for x in raw.splitlines() if x.strip()]

    def new_raw(self) -> str:
        with self.req_log.open("rb") as f:
            f.seek(self.offset)
            return f.read().decode("utf-8")


# ── U9-1 ─────────────────────────────────────────────────────────────────────

def criterion_1(srv: Server, tag: str) -> dict:
    sent, texts = [], []
    sent.append(srv.send("POST", "/ping", {"message": "hello"}))
    sent.append(srv.send("GET", "/health"))
    for i, text in enumerate(scenarios.HUMAN):
        texts.append(text)
        sent.append(srv.send("POST", "/submit", {"text": text, "creator_id": f"u9c1_{tag}_{i}"}))
    cid = sent[2]["body"].get("content_id")
    sent.append(srv.send("POST", "/appeal", {"content_id": cid, "reasoning": "I wrote this."}))
    sent.append(srv.send("POST", "/appeal", {"content_id": cid, "reasoning": "Again."}))
    sent.append(srv.send("POST", "/appeal", {"content_id": "no-such-id", "reasoning": "Testing."}))
    sent.append(srv.send("GET", "/log?limit=5"))
    sent.append(srv.send("GET", "/log?limit=1"))
    sent.append(srv.send("POST", "/submit", raw="this is not json {"))
    sent.append(srv.send("GET", "/no-such-route"))
    sent.append(srv.send("GET", "/health"))

    lines = srv.new_lines()
    raw = srv.new_raw()
    good = 0
    for req, line in zip(sent, lines):
        if (line.get("method") == req["method"] and line.get("path") == req["path"].split("?")[0]
                and set(line) == FIELDS and line["status"] == req["status"]
                and isinstance(line["duration_ms"], (int, float)) and line["duration_ms"] >= 0):
            good += 1
    leaks = sum(1 for t in texts if t[:30] in raw)
    passed = len(sent) == 20 and len(lines) == 20 and good == 20 and leaks == 0
    return {
        "value": f"{len(lines)} lines, {good}/20 complete, {leaks} leaks",
        "passed": passed,
        "requests_sent": len(sent),
        "lines_added": len(lines),
        "complete_and_matching": good,
        "text_leaks": leaks,
        "client_statuses": [r["status"] for r in sent],
        "log_statuses": [l.get("status") for l in lines],
        "lines": lines,
    }


# ── U9-2 ─────────────────────────────────────────────────────────────────────

def criterion_2(srv: Server, tag: str) -> dict:
    sent = []
    malformed = next(s for s in scenarios.SCENARIOS if s.get("criterion") == 5)["bodies"]
    for body in malformed:
        if isinstance(body, str):
            sent.append(srv.send("POST", "/submit", raw=body))
        else:
            sent.append(srv.send("POST", "/submit", body))
    sent.append(srv.send("POST", "/submit", {"text": "ok", "creator_id": f"u9c2_{tag}_short"}))
    sent.append(srv.send("POST", "/appeal", {"content_id": "no-such-id", "reasoning": "Testing."}))
    sent.append(srv.send("GET", "/no-such-route"))
    for _ in range(11):
        sent.append(srv.send("POST", "/submit", {"text": "", "creator_id": f"u9c2_{tag}_flood"}))

    lines = srv.new_lines()
    rows, good = [], 0
    for req, line in zip(sent, lines):
        want_error = req["body"].get("error") or f"http_{req['status']}"
        ok = (line.get("status") == req["status"] and line.get("error") is not None
              and line.get("error") == want_error)
        good += ok
        rows.append({"path": req["path"], "client_status": req["status"], "client_error": want_error,
                     "log_status": line.get("status"), "log_error": line.get("error"), "ok": ok})
    five_xx = sum(1 for l in lines if l.get("status", 0) >= 500)
    flood_codes = [r["status"] for r in sent[-11:]]
    got_429 = any(l.get("status") == 429 and l.get("error") == "rate_limited" for l in lines)
    passed = (len(sent) == 22 and len(lines) == 22 and good == 22 and five_xx == 0 and got_429
              and all(r["status"] < 500 for r in sent))
    return {
        "value": f"{good}/22 match, {five_xx} 5xx, 429 logged: {got_429}",
        "passed": passed,
        "lines_added": len(lines),
        "flood_statuses": flood_codes,
        "rows": rows,
        "lines": lines,
    }


# ── U9-3 ─────────────────────────────────────────────────────────────────────

def criterion_3(srv: Server, tag: str) -> dict:
    srv.send("POST", "/submit", {"text": COST_TEXT, "creator_id": f"u9c3_{tag}_warmup"})
    srv.offset = srv.req_log.stat().st_size      # the warm-up isn't counted
    sent = [srv.send("POST", "/submit", {"text": COST_TEXT, "creator_id": f"u9c3_{tag}_{i}"})
            for i in range(10)]
    lines = srv.new_lines()
    by_id = {l["content_id"]: l for l in lines if l["path"] == "/submit"}
    pairs = []
    for req in sent:
        line = by_id.get(req["body"].get("content_id"), {})
        pairs.append({"status": req["status"], "duration_ms": line.get("duration_ms"),
                      "client_ms": req["client_ms"],
                      "gap_ms": round(req["client_ms"] - line["duration_ms"], 1) if line else None})
    durs = [p["duration_ms"] for p in pairs if p["duration_ms"] is not None]
    gaps = [p["gap_ms"] for p in pairs if p["gap_ms"] is not None]
    mean = round(statistics.mean(durs), 1) if durs else None
    passed = (len(durs) == 10 and all(p["status"] == 200 for p in pairs) and mean <= 300
              and max(durs) <= 500 and all(abs(g) <= 15 for g in gaps))
    return {
        "value": f"mean {mean} ms, max {max(durs) if durs else None} ms, max gap {max(gaps) if gaps else None} ms",
        "passed": passed,
        "mean_ms": mean,
        "max_ms": max(durs) if durs else None,
        "max_gap_ms": max(gaps) if gaps else None,
        "runs": pairs,
        "lines": lines,
    }


# ── U9-4 ─────────────────────────────────────────────────────────────────────

def criterion_4(srv: Server, tag: str) -> dict:
    req = srv.send("POST", "/submit", {"text": COST_TEXT, "creator_id": f"u9c4_{tag}"})
    lines = srv.new_lines()
    line = next((l for l in lines if l["path"] == "/submit"), {})
    passed = req["status"] == 200 and req["client_ms"] <= 1000
    return {
        "value": f"first submit {req['client_ms']} ms (ready after {srv.ready_s:.2f} s)",
        "passed": passed,
        "launch_to_health_s": round(srv.ready_s, 2),
        "first_submit_client_ms": req["client_ms"],
        "first_submit_duration_ms": line.get("duration_ms"),
        "model_loaded_at_first_submit": line.get("model_loaded"),
        "lines": lines,
    }


# ── U9-5 ─────────────────────────────────────────────────────────────────────

def _audit_kind_ok(e: dict) -> bool:
    keys = set(e)
    if e.get("event") is None:
        return keys == NINE
    if e["event"] == "appeal":
        return keys == NINE | {"event", "reasoning"}
    if e["event"] == "rejected":
        extra = {"event", "reason", "http_status"} | ({"limit"} if e.get("reason") == "rate_limited" else set())
        return keys == NINE | extra
    return False


def criterion_5(srv: Server, tag: str, label: str) -> dict:
    audit_offset = config.AUDIT_LOG.stat().st_size if config.AUDIT_LOG.exists() else 0
    proc = subprocess.run(
        [sys.executable, "run_eval.py", "--trials", "1", "--label", f"unit9_{tag}",
         "--url", srv.base],
        cwd=ROOT, capture_output=True, text=True, timeout=1800,
    )
    out = proc.stdout
    held = {}
    for m in re.finditer(r"\(criterion (\d)\)\n\s+trial 1: .*\n\s+(.+?)  (held|MISSED)", out):
        held[int(m.group(1))] = {"value": m.group(2).strip(), "held": m.group(3) == "held"}
    with config.AUDIT_LOG.open("rb") as f:
        f.seek(audit_offset)
        added = [json.loads(x) for x in f.read().decode("utf-8").splitlines() if x.strip()]
    bad_shape = [e for e in added if not _audit_kind_ok(e)]

    tests = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"],
                           cwd=ROOT, capture_output=True, text=True, timeout=900)
    ran = re.search(r"Ran (\d+) tests", tests.stderr)
    gap = held.get(2, {}).get("value", "")
    results_file = re.search(r"Wrote (\S+)", out)

    passed = (all(held.get(c, {}).get("held") for c in (1, 3, 4, 5))
              and gap == "gap 0.201" and not bad_shape and len(added) > 0
              and tests.returncode == 0)
    return {
        "value": (f"c1/3/4/5 held: {[held.get(c, {}).get('held') for c in (1, 3, 4, 5)]}, "
                  f"{gap}, {len(added) - len(bad_shape)}/{len(added)} audit lines right shape, "
                  f"tests {'OK' if tests.returncode == 0 else 'FAILED'} ({ran.group(1) if ran else '?'})"),
        "passed": passed,
        "run_eval_criteria": held,
        "run_eval_results_file": results_file.group(1) if results_file else None,
        "audit_lines_added": len(added),
        "audit_lines_wrong_shape": bad_shape[:5],
        "unit_tests": tests.stderr.strip().splitlines()[-3:],
        "request_log_lines_added": len(srv.new_lines()),
    }


CRITERIA = {
    1: ("Every request leaves one complete log line", "20 lines, 20/20 complete and matching, 0 text leaks"),
    2: ("Every refused request says why", "22/22 status and error match, 0 5xx, 429 logged"),
    3: ("Warm requests cheap, logged time honest", "mean ≤ 300 ms, max ≤ 500 ms, each within 15 ms of client"),
    4: ("First request after a start isn't cold", "first /submit ≤ 1.0 s after /health answers"),
    5: ("Unit 8 behaviour unchanged under gunicorn", "c1/3/4/5 held, gap 0.201, audit shapes, all tests pass"),
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--label", required=True)
    ap.add_argument("--trials", type=int, default=3)
    ap.add_argument("--only", type=int, action="append")
    ap.add_argument("--port", type=int, default=5050)
    args = ap.parse_args()

    req_log = config.LOG_DIR / f"requests_unit9_{args.label}.jsonl"
    which = args.only or sorted(CRITERIA)
    results = {}
    for c in which:
        print(f"\nU9-{c}: {CRITERIA[c][0]}")
        results[c] = []
        for t in range(1, args.trials + 1):
            tag = f"{args.label}_t{t}"
            with Server(args.port, req_log) as srv:
                if c == 5:
                    outcome = criterion_5(srv, tag, args.label)
                else:
                    outcome = globals()[f"criterion_{c}"](srv, tag)
            outcome["trial"] = t
            results[c].append(outcome)
            print(f"  trial {t}: {outcome['value']}  {'held' if outcome['passed'] else 'MISSED'}")

    write_report(results, args, req_log)


def write_report(results, args, req_log):
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    path = config.RESULTS_DIR / f"unit9_{args.label}_{stamp}.md"
    n = args.trials
    lines = [f"# Unit 9 criteria, {args.label}", "",
             "- Produced by: `run_ops_eval.py::main`; each trial is a fresh `gunicorn app:app` "
             f"on port {args.port}",
             f"- Request log for this run: `{req_log.relative_to(ROOT)}`",
             f"- {n} trials per criterion, {dt.datetime.now():%Y-%m-%d %H:%M}", "",
             f"| Criterion | Target | {' | '.join(f'Trial {i}' for i in range(1, n + 1))} | Verdict |",
             f"|---|---|{'|'.join(['---'] * n)}|---|"]
    for c, outs in results.items():
        cells = [f"{o['value']} ({'held' if o['passed'] else 'missed'})" for o in outs]
        verdict = "MET" if all(o["passed"] for o in outs) else "MISSED"
        lines.append(f"| U9-{c}. {CRITERIA[c][0]} | {CRITERIA[c][1]} | {' | '.join(cells)} | {verdict} |")
    lines += ["", "## Every trial, as measured", ""]
    for c, outs in results.items():
        lines += [f"### U9-{c}. {CRITERIA[c][0]}", "",
                  f"Check: `run_ops_eval.py::criterion_{c}`", ""]
        for o in outs:
            detail = {k: v for k, v in o.items() if k != "lines"}
            lines += [f"**Trial {o['trial']}**", "", "```json", json.dumps(detail, indent=2), "```", ""]
            if o.get("lines"):
                lines += ["Request-log lines this check read:", "", "```json"]
                lines += [json.dumps(l) for l in o["lines"]]
                lines += ["```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
