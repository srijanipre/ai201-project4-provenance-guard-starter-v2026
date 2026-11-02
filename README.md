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
| 1. False positives on human writing | ≤ 1 of 10 labelled high-confidence AI, every run | 0/10 | 0/10 | 0/10 | **MET** |
| 2. AI and human separate | mean AI − mean human ≥ 0.30 | 0.145 | 0.145 | 0.145 | **MISSED** |
| 3. All three labels reachable | all 3 labels from real text, and 6/6 boundary checks | 3 labels, 6/6 | 3 labels, 6/6 | 3 labels, 6/6 | **MET** |
| 4. Appeals change status and are logged | 5/5 appeals, 3/3 error cases | 5/5, 3/3 | 5/5, 3/3 | 5/5, 3/3 | **MET** |
| 5. Malformed input refused cleanly | 8/8 4xx with `error`, none 5xx, 0 decision entries | 8/8, 0 | 8/8, 0 | 8/8, 0 | **MET** |

Each verdict is against the original target in `criteria.md`, and it holds
only if all three trials hit it. Nothing in `criteria.md` was changed. All
five criteria could be measured as written, so there's no revision.

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

**Broken attacks:** none diagnosed yet. The attack set is missing (see
**Attack Run — Before**), so there are no HELD or BROKE verdicts to diagnose.

**Criterion 2 — MISSED (gap 0.145 against 0.30, all three trials).**
Stages: **signal one** and **signal two**, not the combining rule or the label
mapping.

Mean scores over the 5 AI and 10 human passages, from the before run:

| | mean AI | mean human | gap |
|---|---|---|---|
| signal one (model) | 0.7145 | 0.5157 | **0.199** |
| signal two (style) | 0.4200 | 0.3547 | **0.065** |
| combined (0.6 / 0.4) | 0.5967 | 0.4513 | **0.145** |

- **Signal one is short on its own.** gpt2 separates the groups by 0.199.
  Formal human prose is the problem. The five Mill and Thoreau passages
  average 0.589 on the model signal (one, `human_formal[1]`, scores 0.748),
  against 0.442 for the plain passages and 0.715 for the AI ones. Formal
  writing uses long, conventional constructions that gpt2 predicts well, so
  it reads as machine-like.
- **Signal two barely separates, because one of its three parts runs
  backwards.** Breaking the style score into its components (mean AI-ish
  component value, AI minus human):

  | component | AI | human | gap |
  |---|---|---|---|
  | sentence-length spread | 0.819 | 0.538 | **+0.281** |
  | punctuation density | 0.357 | 0.231 | **+0.126** |
  | type-token ratio | 0.084 | 0.295 | **−0.211** |

  The AI passages have a *higher* moving-average TTR (0.871) than the human
  ones (0.782). The component assumes the reverse, so it marks the AI text as
  human-like by 0.211 and cancels most of what the other two measure. Without
  it, the style gap on the same passages is 0.203.
- **The combining rule isn't the cause.** A weighted average can't separate
  the groups more than its best input does. Even putting all the weight on
  the model signal gives 0.199, still under 0.30. The 0.6 / 0.4 weights pull
  the gap down to 0.145 only because the style signal is so weak.
- **The label mapping is irrelevant.** The criterion is about combined
  scores, before any label is chosen.

**Pattern across the results.** The miss and the near-misses come from one
place: formal human prose and fluent AI prose look alike to both signals. On
the model signal, formal human writing is predictable. On the style signal,
formal writing has flat sentence lengths, and the AI passages have a varied
vocabulary. The criteria that pass (3, 4, 5) test the route and the label
mapping, which work. The two that test the signals (1 and 2) either miss or
pass only because the 0.70 AI threshold is high.

**Criterion 1 passes, but by threshold, not by separation.** 0 of 10 human
passages got the AI label, but 8 of 10 landed in unsure. The closest was
`human_formal[1]` at 0.5958, 0.10 under the AI bar. The same high threshold
leaves 4 of 5 clearly AI passages in unsure too (`ai_clear[0]` at 0.5072,
`ai_clear[3]` at 0.4753). The system avoids false accusations mostly by
declining to decide.



---

## The Improvement

**What I changed:** I took the type-token ratio component out of the style
signal. `stylometry.py::style_signal` now averages two components, sentence
spread and punctuation, where it used to average three. `type_token_ratio`
itself is still there and still printed by `python stylometry.py`. It just
doesn't count. Nothing else changed: the model signal, the 0.6 / 0.4 weights,
the 0.35 / 0.70 thresholds and the label text are all as they were in the
before run.

**Which diagnosis pointed at it:** criterion 2's. The TTR component ran
backwards on the calibration passages. It scored the AI text as more
human-like than the human text by 0.211, and that wiped out most of the style
signal's 0.281 + 0.126 from the other two components. Of the three stages that
could move the gap, it was the only one with a component pointing the wrong
way. Reweighting couldn't fix it either, since even all the weight on the
model signal tops out at 0.199.

I dropped it rather than flipped it. Flipping would claim that higher
vocabulary variety means AI, and 15 passages aren't enough to support that.
Dropping it only claims that this measure isn't helping here.

**A caveat that matters:** the change was chosen by looking at the same 15
calibration passages that criteria 1–3 then re-measure. So the after numbers
are in-sample. They show the change does what the diagnosis predicted. They
don't show it generalises. The attack set would have been the out-of-sample
check.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

> **Blocked, same as the before run:** the attack set isn't available, so
> there's no before or after attack table to compare. With the files in
> `attacks/` it's `PORT=5050 python run_attacks.py --set attacks --label
> after`. The before run would need the commit before this change checked out
> first.

### Criteria — before and after, side by side

`results/run_2026-11-01_2129_before.md` against
`results/run_2026-11-01_2133_after.md`, three trials each. All three trials
were identical again in both runs.

| Criterion | Target | Before (×3) | After (×3) | Before | After |
|---|---|---|---|---|---|
| 1. False positives | ≤ 1 of 10 | 0/10 | 0/10 | MET | MET |
| 2. Separation | gap ≥ 0.30 | 0.145 | **0.201** | MISSED | MISSED |
| 3. Labels reachable | 3 labels, 6/6 | ai 1 · unsure 15 · human 3; 6/6 | ai **2** · unsure 14 · human 3; 6/6 | MET | MET |
| 4. Appeals | 5/5, 3/3 | 5/5, 3/3 | 5/5, 3/3 | MET | MET |
| 5. Malformed input | 8/8, 0 decisions | 8/8, 0 | 8/8, 0 | MET | MET |

Per passage, criterion 2's run (trial 1 of each):

| Passage | style before → after | combined before → after | label before → after |
|---|---|---|---|
| ai_clear[0] | 0.4393 → 0.6113 | 0.5072 → 0.5760 | unsure → unsure |
| ai_clear[1] | 0.5043 → 0.6184 | 0.7380 → 0.7836 | ai → ai |
| ai_clear[2] | 0.4423 → 0.6384 | 0.6537 → 0.7322 | unsure → **ai** |
| ai_clear[3] | 0.2946 → 0.4419 | 0.4753 → 0.5342 | unsure → unsure |
| ai_clear[4] | 0.4193 → 0.6290 | 0.6091 → 0.6930 | unsure → unsure |
| human_plain[0] | 0.2386 → 0.1316 | 0.3413 → 0.2985 | human → human |
| human_plain[1] | 0.4386 → 0.4896 | 0.4569 → 0.4773 | unsure → unsure |
| human_plain[2] | 0.2568 → 0.2881 | 0.4097 → 0.4223 | unsure → unsure |
| human_plain[3] | 0.2618 → 0.2822 | 0.2572 → 0.2653 | human → human |
| human_plain[4] | 0.2661 → 0.2500 | 0.4458 → 0.4394 | unsure → unsure |
| human_formal[0] | 0.4142 → 0.5101 | 0.5389 → 0.5772 | unsure → unsure |
| human_formal[1] | 0.3673 → 0.4228 | 0.5958 → **0.6180** | unsure → unsure |
| human_formal[2] | 0.4459 → 0.5444 | 0.5374 → 0.5768 | unsure → unsure |
| human_formal[3] | 0.5206 → 0.5194 | 0.5670 → 0.5666 | unsure → unsure |
| human_formal[4] | 0.3368 → 0.4063 | 0.3630 → 0.3908 | unsure → unsure |
| **mean AI / mean human** | | **0.5967 / 0.4513 → 0.6638 / 0.4632** | |

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

Partly. It moved the number it was aimed at, and it cost something on the
side that matters more.

- **Improved:** the gap went from 0.145 to 0.201 in all three trials, as the
  component arithmetic predicted (0.6 × 0.199 + 0.4 × 0.203 = 0.201). Mean AI
  rose by 0.067 and mean human by only 0.012. One more clearly AI passage
  (`ai_clear[2]`, 0.6537 → 0.7322) now gets the AI label. Across the 19
  calibration passages, AI labels went from 1 to 2.
- **Still missed:** criterion 2 is still 0.10 short of 0.30. The model signal
  caps what any style fix can do, and formal human prose still averages
  0.589 on it.
- **Regression:** human scores went *up*, not down. Mean human rose from
  0.4513 to 0.4632, and the closest human passage to the AI bar,
  `human_formal[1]`, went from 0.5958 to 0.6180. Its margin under 0.70 shrank
  from 0.104 to 0.082. Criterion 1 still holds at 0/10, but with less room.
  Dropping TTR removed a component that happened to read formal human text as
  human-like, for the wrong reason, so formal writers lost a cushion they
  never should have relied on.
- **Unchanged:** criteria 3, 4 and 5 are identical, as expected for a change
  that only touches signal two. The 26 unit tests still pass.

The trade, in one line: AI detection got better on the calibration set, and
the highest-scoring human passage moved 0.022 closer to being called AI.

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
