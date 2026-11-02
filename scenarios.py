"""
What your test runs. ← UNIT 8, MILESTONE 3

One scenario per criterion in criteria.md. `run_eval.py` sends each one three
times and then calls the scenario's `check`, which turns that trial's responses
into the number the criterion names and says whether the target held.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you.

    "bodies"  a list of whole request bodies, sent exactly as written. A dict is
              sent as JSON; a str is sent as raw bytes claiming to be JSON, which
              is the only way to send a body that doesn't parse.

The texts come from samples/calibration.json, the set criteria 1–3 were written
against. The human passages are public-domain books published before 2020; the
AI passages were written by Claude for that set.

Criterion 4 can't be tested by sending text alone, so its check submits first
and then appeals against the content_ids that came back. Criterion 3's
boundary half calls scoring.score_to_label directly, since it's about exact
scores no real text will land on.
"""

import json
from pathlib import Path

import config
import scoring

_CALIBRATION = json.loads(
    (Path(__file__).parent / "samples" / "calibration.json").read_text(encoding="utf-8")
)


def _texts(group):
    return [sample["text"] for sample in _CALIBRATION[group]]


HUMAN = _texts("human_plain") + _texts("human_formal")      # 10, criterion 1
AI_CLEAR = _texts("ai_clear")                                # 5, criterion 2
ALL_SAMPLES = (HUMAN + _texts("borderline") + AI_CLEAR
               + _texts("ai_light_edit"))                    # 19, criterion 3


# ── Checks ───────────────────────────────────────────────────────────────────
# Each takes one trial's results (one dict per request, in order) and a `ctx`
# with the service URL and a `requests` session, and returns
#     {"value": <short text for the run-log table>, "passed": bool, ...detail}

def _decisions(log):
    return [e for e in log if e.get("event") is None]


def check_false_positives(results, ctx):
    """Criterion 1: at most 1 of 10 human passages labelled high-confidence AI."""
    scored = [r for r in results if r["status"] == 200]
    flagged = sum(1 for r in scored if r["guess"] == "ai")
    return {
        "value": f"{flagged}/{len(results)} AI",
        "passed": len(scored) == len(results) and flagged <= 1,
        "false_positives": flagged,
        "guesses": [r["guess"] for r in results],
    }


def check_separation(results, ctx):
    """Criterion 2: mean combined score of AI minus mean of human >= 0.30."""
    groups = {"ai": [], "human": []}
    for result, group in zip(results, SEPARATION_GROUPS):
        if result["status"] == 200:
            groups[group].append(result["confidence"])
    mean_ai = sum(groups["ai"]) / len(groups["ai"])
    mean_human = sum(groups["human"]) / len(groups["human"])
    gap = mean_ai - mean_human
    return {
        "value": f"gap {gap:.3f}",
        "passed": len(groups["ai"]) == 5 and len(groups["human"]) == 10 and gap >= 0.30,
        "mean_ai": round(mean_ai, 4),
        "mean_human": round(mean_human, 4),
        "gap": round(gap, 4),
    }


def check_label_coverage(results, ctx):
    """Criterion 3: all three labels from real text, and 6 of 6 boundary checks."""
    seen = {}
    for r in results:
        if r["status"] == 200:
            seen[r["guess"]] = seen.get(r["guess"], 0) + 1

    h, a = config.HUMAN_THRESHOLD, config.AI_THRESHOLD
    boundaries = [(0.0, "human"), (round(h - 0.0001, 4), "human"), (h, "unsure"),
                  (round(a - 0.0001, 4), "unsure"), (a, "ai"), (1.0, "ai")]
    boundary_results = [
        {"score": score, "want": want, "got": scoring.score_to_label(score)[0]}
        for score, want in boundaries
    ]
    passed_boundaries = sum(1 for b in boundary_results if b["got"] == b["want"])
    labels_reached = sorted(seen)
    return {
        "value": f"{len(labels_reached)}/3 labels, {passed_boundaries}/6 bounds",
        "passed": set(labels_reached) == {"ai", "human", "unsure"} and passed_boundaries == 6,
        "labels_seen": seen,
        "boundaries": boundary_results,
    }


def check_appeals(results, ctx):
    """
    Criterion 4: 5 of 5 appeals change status and log exactly one appeal
    entry with the original decision untouched, and 3 of 3 error cases
    (unknown id → 404 with no new lines, repeat appeal → 409, malformed appeal
    body → 400) behave.
    """
    url, http = ctx["url"], ctx["http"]
    submitted = [r for r in results if r["status"] == 200]
    appeals = []
    for r in submitted:
        cid = r["content_id"]
        before = ctx["read_log"]()
        original = [e for e in _decisions(before) if e.get("content_id") == cid]
        resp = http.post(f"{url}/appeal", json={
            "content_id": cid,
            "reasoning": "I wrote this myself and can share my drafts.",
        }, timeout=ctx["timeout"])
        after = ctx["read_log"]()
        added = after[len(before):]
        appeals.append({
            "content_id": cid,
            "guess": r["guess"],
            "http": resp.status_code,
            "status": (resp.json() or {}).get("status"),
            "lines_added": len(added),
            "appeal_entry": len(added) == 1 and added[0].get("event") == "appeal"
                            and added[0].get("content_id") == cid,
            "original_intact": bool(original) and original == [
                e for e in _decisions(after) if e.get("content_id") == cid],
        })
    ok_appeals = sum(1 for a in appeals if a["http"] == 200 and a["status"] == "under_review"
                     and a["lines_added"] == 1 and a["appeal_entry"] and a["original_intact"])

    errors = []
    before = len(ctx["read_log"]())
    resp = http.post(f"{url}/appeal", json={"content_id": "no-such-id-0000",
                                            "reasoning": "Testing an unknown id."},
                     timeout=ctx["timeout"])
    added = len(ctx["read_log"]()) - before
    errors.append({"case": "unknown content_id", "http": resp.status_code,
                   "lines_added": added, "ok": resp.status_code == 404 and added == 0})

    if submitted:
        resp = http.post(f"{url}/appeal", json={"content_id": submitted[0]["content_id"],
                                                "reasoning": "Appealing again."},
                         timeout=ctx["timeout"])
        errors.append({"case": "second appeal", "http": resp.status_code,
                       "ok": resp.status_code == 409})

    # No reasoning field, so this should be refused with a 400.
    bad_body = {}
    if submitted:
        bad_body = {"content_id": submitted[0]["content_id"]}
    resp = http.post(f"{url}/appeal", json=bad_body, timeout=ctx["timeout"])
    body = resp.json() if resp.content else {}
    errors.append({"case": "malformed body (no reasoning)", "http": resp.status_code,
                   "ok": resp.status_code == 400 and "error" in body})
    ok_errors = sum(1 for e in errors if e["ok"])

    labels = sorted({a["guess"] for a in appeals})
    return {
        "value": f"{ok_appeals}/5 appeals, {ok_errors}/3 errors",
        "passed": ok_appeals == 5 and ok_errors == 3 and len(labels) >= 2,
        "labels_appealed": labels,
        "appeals": appeals,
        "error_cases": errors,
    }


def check_malformed(results, ctx):
    """
    Criterion 5: all 8 malformed requests get a 4xx with a JSON `error` key,
    none get a 5xx, and none add a decision entry to the log.
    """
    clean = sum(1 for r in results
                if r["status"] is not None and 400 <= r["status"] < 500 and r.get("has_error_key"))
    decisions_added = len(_decisions(ctx["log_added"]))
    return {
        "value": f"{clean}/8 clean, {decisions_added} decisions logged",
        "passed": clean == 8 and decisions_added == 0,
        "statuses": [r["status"] for r in results],
        "decision_entries_added": decisions_added,
        "rejected_entries_added": sum(1 for e in ctx["log_added"] if e.get("event") == "rejected"),
    }


# ── The five scenarios ───────────────────────────────────────────────────────

SEPARATION_GROUPS = ["ai"] * len(AI_CLEAR) + ["human"] * len(HUMAN)

# One of each kind from the unit 7 run: ai_clear[1] scored ai, human_plain[0]
# and [3] scored human, ai_clear[0] and human_formal[1] scored unsure. The check
# confirms at run time that at least two labels were actually appealed.
APPEAL_TEXTS = [
    _texts("ai_clear")[1],
    _texts("human_plain")[0],
    _texts("ai_clear")[0],
    _texts("human_plain")[3],
    _texts("human_formal")[1],
]

SCENARIOS = [
    {
        "name": "human passages",
        "criterion": 1,
        "target": "≤ 1 of 10 labelled AI, every run",
        "texts": HUMAN,
        "check": check_false_positives,
    },
    {
        "name": "AI vs human separation",
        "criterion": 2,
        "target": "mean AI − mean human ≥ 0.30",
        "texts": AI_CLEAR + HUMAN,
        "check": check_separation,
    },
    {
        "name": "label coverage",
        "criterion": 3,
        "target": "all 3 labels from real text; 6/6 boundary checks",
        "texts": ALL_SAMPLES,
        "check": check_label_coverage,
    },
    {
        "name": "appeal path",
        "criterion": 4,
        "target": "5/5 appeals; 3/3 error cases",
        "texts": APPEAL_TEXTS,
        "check": check_appeals,
    },
    {
        "name": "malformed input",
        "criterion": 5,
        "target": "8/8 4xx with `error`, 0 decisions logged",
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "   \n\t ", "creator_id": "eval_bad_space"},
            {"creator_id": "eval_bad_missing"},
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": 12345, "creator_id": "eval_bad_number"},
            {"text": "A perfectly ordinary sentence with no creator attached to it."},
            {"text": "word " * 2500, "creator_id": "eval_bad_huge"},
            "this is not json {",
        ],
        "check": check_malformed,
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, (dict, str)):
                    problems.append(
                        f"scenario {i}, body {j} is neither a dict nor a raw string"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
