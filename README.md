# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**

**Why that might differ between human and AI writing:**

**What it can't see:**

### Signal two — the style signal

**What it measures:**

**Why that might differ between human and AI writing:**

**What it can't see:**

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**

**The numbers:**

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "...", "creator_id": "..."}'
```

```json

```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json

```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 100 per day (`config.py`, applied by the
`@limiter.limit(...)` decorator on `app.py::submit`)

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

A real writer submits a piece, maybe revises it and resubmits a few times. Even
someone fixing typos and resubmitting quickly rarely needs more than a handful
in one minute, so 10 a minute doesn't get in their way. A heavy real day is a
few dozen submissions, and 100 a day is well past that.

A script mapping my thresholds needs hundreds of near-identical probes. At 10 a
minute that's slow, and at 100 a day one caller can't map much in a day. The
limit also protects the expensive part: every accepted request runs gpt2.

I left the starter's 10/minute and lowered the daily cap from 200 to 100. 200 a
day is far more than a writer needs and doubles what one caller can probe.

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

Per `creator_id`, falling back to the caller's address when the body has no
usable `creator_id` (`app.py::rate_limit_key`). Every request to `/submit`
counts, including ones refused with a 4xx.

The weakness: `creator_id` is whatever the caller sends, with no account
behind it. A script that invents a new `creator_id` per request is never
limited. That's exactly how the attack set looks (`attacker_<id>` per row).
Per-address limiting would catch that but would lump a whole household or
classroom behind one NAT into one caller. Fixing it properly needs real
accounts, which this service doesn't have.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
$ python run_attacks.py --flood 15     # service on port 5050, see note below
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429

5 of 15 were rate limited.
Wrote results/flood_2026-11-01_2127.md
```

The 11th request onwards gets a 429 with a JSON body:

```json
{"error": "rate_limited", "message": "Too many submissions. Try again shortly.", "limit": "10 per 1 minute"}
```

Each 429 is written to the audit log (`GET /log`):

```json
{"combined_score": null, "content_id": null, "creator_id": "flood_tester", "event": "rejected", "guess": null, "http_status": 429, "label": null, "limit": "10 per 1 minute", "model_score": null, "reason": "rate_limited", "status": "rejected", "style_score": null, "timestamp": "2026-11-02T03:27:04+00:00"}
```

**Rejected requests are logged too.** Any `/submit` request refused with a
4xx or 5xx writes a `rejected` entry with the reason and HTTP status. Every
entry, whether decision, appeal or rejection, carries all nine fields:
`timestamp`, `content_id`, `creator_id`, `guess`, `model_score`,
`style_score`, `combined_score`, `label`, `status`. Fields a rejection never
computed are `null`. An appeal entry copies the guess, scores and label of
the decision it's appealing. A bad request to `/appeal` still writes nothing,
because criterion 4 requires a 404 appeal to add zero lines.

```json
{"combined_score": null, "content_id": null, "creator_id": "m1_check", "event": "rejected", "guess": null, "http_status": 400, "label": null, "model_score": null, "reason": "empty_text", "status": "rejected", "style_score": null, "timestamp": "2026-11-02T03:27:13+00:00"}
```

> **Note on ports:** an old debug-mode `app.py` from unit 7 was still holding
> port 5000, so unit 8 runs used a fresh instance on port 5050 (`PORT=5050`).
> `results/flood_2026-11-01_2126.md` is an earlier identical flood that hit
> that old server after its auto-reloader had picked up the same code. Both
> show 10 × 200 then 5 × 429.

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

> **Blocked: the attack set isn't in this repository.** `run_attacks.py
> --set <folder>` needs the staff-provided `attacks.csv` and
> `attacks_malformed_requests.csv`. Neither is in the repo or its history, and
> neither is anywhere on this machine. I haven't written stand-in attacks,
> because a set I wrote myself would test what I already thought of, not what
> staff built from the blind spots. The table, the HELD/BROKE count, the ten
> audit entries from the run and the worst outcome all wait on those two
> files.
>
> Once they're in place (for example in `attacks/`), with the service on port
> 5050 and the code as it was before the improvement (commit before "The
> Improvement" below):
>
> ```bash
> PORT=5050 python run_attacks.py --set attacks --label before
> ```

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

*Not from the attack run, which is blocked.* These ten are real entries from
`logs/audit.jsonl`, written during the "before" criteria run
(2026-11-02 03:29 UTC). They cover a correct AI call, two formal human passages
sitting high in unsure, an AI passage the system missed, an appeal, and four
rejections. The 429 rejections are under **Rate Limiting**. They should be
swapped for attack-run entries once that run exists.

```json
{"timestamp": "2026-11-02T03:29:33+00:00", "content_id": "c4271e0e-a769-44d2-b333-686647860018", "creator_id": "eval_AI vs human _2", "guess": "ai", "model_score": 0.8938, "style_score": 0.5043, "combined_score": 0.738, "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.", "status": "decided"}
{"timestamp": "2026-11-02T03:29:30+00:00", "content_id": "a581b53b-3ba7-411c-8bba-afa5e29e09ae", "creator_id": "eval_human passag_7", "guess": "unsure", "model_score": 0.7481, "style_score": 0.3673, "combined_score": 0.5958, "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.", "status": "decided"}
{"timestamp": "2026-11-02T03:29:31+00:00", "content_id": "164a964b-5670-4def-bc53-da468c45f1a7", "creator_id": "eval_human passag_9", "guess": "unsure", "model_score": 0.598, "style_score": 0.5206, "combined_score": 0.567, "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.", "status": "decided"}
{"timestamp": "2026-11-02T03:29:33+00:00", "content_id": "144cd20b-87d0-41a4-b375-29a61caabef5", "creator_id": "eval_AI vs human _1", "guess": "unsure", "model_score": 0.5525, "style_score": 0.4393, "combined_score": 0.5072, "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.", "status": "decided"}
{"timestamp": "2026-11-02T03:29:30+00:00", "content_id": "c4f9deb2-90c9-47df-bf39-726ba5fe5717", "creator_id": "eval_human passag_1", "guess": "human", "model_score": 0.4097, "style_score": 0.2386, "combined_score": 0.3413, "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.", "status": "decided"}
{"timestamp": "2026-11-02T03:29:44+00:00", "content_id": "29d7d54a-ecaf-4faf-a01b-6520f1334af8", "creator_id": "eval_appeal path_1", "guess": "ai", "model_score": 0.8938, "style_score": 0.5043, "combined_score": 0.738, "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.", "status": "under_review", "event": "appeal", "reasoning": "I wrote this myself and can share my drafts."}
{"timestamp": "2026-11-02T03:29:45+00:00", "content_id": null, "creator_id": "eval_bad_empty", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "rejected", "event": "rejected", "reason": "empty_text", "http_status": 400}
{"timestamp": "2026-11-02T03:29:45+00:00", "content_id": null, "creator_id": "unknown", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "rejected", "event": "rejected", "reason": "invalid_body", "http_status": 400}
{"timestamp": "2026-11-02T03:29:45+00:00", "content_id": null, "creator_id": "eval_bad_huge", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "rejected", "event": "rejected", "reason": "text_too_long", "http_status": 413}
{"timestamp": "2026-11-02T03:29:45+00:00", "content_id": null, "creator_id": "eval_bad_missing", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "rejected", "event": "rejected", "reason": "missing_field", "http_status": 400}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

*Pending the attack run.*


---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

`results/run_2026-11-01_2129_before.md`. Every criterion is measured as
written in `criteria.md`. Each one has a scenario in `scenarios.py`, and that
scenario's `check_*` function turns a trial's responses into the criterion's
number. I extended `run_eval.py` to run those checks, to send a non-JSON body
raw, and to diff `GET /log` around each trial, so criteria 4 and 5 are
checked against the live log and not by hand.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives on human writing | ≤ 1 of 10 labelled high-confidence AI, every run | 0/10 | 0/10 | 0/10 |  |
| 2. AI and human separate | mean AI − mean human ≥ 0.30 | 0.145 | 0.145 | 0.145 |  |
| 3. All three labels reachable | all 3 labels from real text, and 6/6 boundary checks | 3 labels, 6/6 | 3 labels, 6/6 | 3 labels, 6/6 |  |
| 4. Appeals change status and are logged | 5/5 appeals, 3/3 error cases | 5/5, 3/3 | 5/5, 3/3 | 5/5, 3/3 |  |
| 5. Malformed input refused cleanly | 8/8 4xx with `error`, none 5xx, 0 decision entries | 8/8, 0 | 8/8, 0 | 8/8, 0 |  |

**The three trials are identical to four decimal places.** gpt2 runs in eval
mode with no sampling, so the same text gives the same perplexity on the same
machine. The three trials do show the result isn't a one-off. They don't add
any spread.

**Criterion 1 uses public-domain passages, not my own writing.** That's how
the criterion was written in unit 7 (5 plain and 5 formal passages from books
published before 2020), so it's measured that way here. The course template
suggests your own writing for this one. That would be a different criterion,
and it would need samples only I can provide.

**Real output from one trial**, pasted as text, naming the file and function
that produced it. All from trial 1 of `results/run_2026-11-01_2129_before.md`,
produced by `run_eval.py::main` (the response rows) and the named
`scenarios.py` check. The rows are excerpts: the full lists are in the results
file.

*Criterion 1:* `scenarios.py::check_false_positives`, plus the first two of
the ten responses

```json
{"value": "0/10 AI", "passed": true, "false_positives": 0,
 "guesses": ["human", "unsure", "unsure", "human", "unsure", "unsure", "unsure", "unsure", "unsure", "unsure"]}
```

```json
[
  {"status": 200, "content_id": "c4f9deb2-90c9-47df-bf39-726ba5fe5717", "guess": "human", "confidence": 0.3413,
   "model_score": 0.4097, "style_score": 0.2386, "sent": "You don’t know about me without you have read a book by the name of Th"},
  {"status": 200, "content_id": "388f7fcb-aa11-4c88-be38-7a2d5a02a1e6", "guess": "unsure", "confidence": 0.4569,
   "model_score": 0.4691, "style_score": 0.4386, "sent": "After supper she got out her book and learned me about Moses and the B"}
]
```

*Criterion 2:* `scenarios.py::check_separation`

```json
{"value": "gap 0.145", "passed": false, "mean_ai": 0.5967, "mean_human": 0.4513, "gap": 0.1454}
```

*Criterion 3:* `scenarios.py::check_label_coverage`

```json
{"value": "3/3 labels, 6/6 bounds", "passed": true,
 "labels_seen": {"human": 3, "unsure": 15, "ai": 1},
 "boundaries": [
   {"score": 0.0, "want": "human", "got": "human"},
   {"score": 0.3499, "want": "human", "got": "human"},
   {"score": 0.35, "want": "unsure", "got": "unsure"},
   {"score": 0.6999, "want": "unsure", "got": "unsure"},
   {"score": 0.7, "want": "ai", "got": "ai"},
   {"score": 1.0, "want": "ai", "got": "ai"}]}
```

*Criterion 4:* `scenarios.py::check_appeals` (first two of five appeals)

```json
{"value": "5/5 appeals, 3/3 errors", "passed": true, "labels_appealed": ["ai", "human", "unsure"],
 "appeals": [
   {"content_id": "29d7d54a-ecaf-4faf-a01b-6520f1334af8", "guess": "ai", "http": 200, "status": "under_review",
    "lines_added": 1, "appeal_entry": true, "original_intact": true},
   {"content_id": "2266338a-0fa6-4fb6-83f7-64a81b42edfb", "guess": "human", "http": 200, "status": "under_review",
    "lines_added": 1, "appeal_entry": true, "original_intact": true}],
 "error_cases": [
   {"case": "unknown content_id", "http": 404, "lines_added": 0, "ok": true},
   {"case": "second appeal", "http": 409, "ok": true},
   {"case": "malformed body (no reasoning)", "http": 400, "ok": true}]}
```

The malformed appeal body, which unit 7 only covered with a unit test, now
runs live in every trial.

*Criterion 5:* `scenarios.py::check_malformed`

```json
{"value": "8/8 clean, 0 decisions logged", "passed": true,
 "statuses": [400, 400, 400, 400, 400, 400, 413, 400],
 "decision_entries_added": 0, "rejected_entries_added": 8}
```

Each of the eight now leaves a `rejected` entry (Milestone 1). The criterion
only forbids *decision* entries, and none were written.

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
