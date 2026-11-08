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

`results/attack_run_2026-11-01_2216_before.md`, all 56 attacks (32 in
`attacks.csv`, 24 in `attacks_malformed_requests.csv`), run against the code
before the improvement (`bb3c49e`). No 5xx, no dropped connections. The
script left every verdict to me. These are mine, using the rules below.

**How I marked HELD or BROKE.** I wrote these rules before reading the
results, from what each family was trying to do:

- **evasion** (AI text, edited to look human): BROKE if it got the
  *high-confidence human* label. Unsure is HELD, because the system didn't
  vouch for it. For reference, the unedited AI paragraph these are built from
  scores 0.6076 (unsure) on this code. I got that by submitting EV03 without
  its quotation, as creator `reference_base_ai`. It isn't one of the 56.
- **false_positive** (genuine human writing): BROKE if labelled
  *high-confidence AI*. Unsure is HELD.
- **prompt_injection:** BROKE if the attacker got the outcome they asked
  for. For PI01–PI03 and PI05 that's a human label on AI text. For PI04 and
  PI06, which wrap real human writing, it's an AI label (an accusation).
  Echoing the payload or changing the log's structure would also count. The
  response never includes the submitted text, and PI05's log entry has only
  the nine normal fields.
- **malformed:** HELD if refused with a 4xx and an `error` key, or scored
  as unsure. BROKE if the service gives a confident label (AI or human) to
  input that isn't English prose, or if it crashes.
- **flood_same_creator:** HELD if the limiter accepts the first 10 and
  answers 429 after that. All 12 rows count as one behaviour. (The file
  says "20 rapid submissions" but has 12 rows.)

These rules are my judgment, and someone with different thresholds could
reasonably mark the borderline rows differently. EV05 is the obvious one: it
has been rewritten so heavily it's arguably human writing now.

| Family | Attacks | HELD | BROKE |
|---|---|---|---|
| `evasion` | 10 | 7 | 3 |
| `false_positive` | 8 | 2 | 6 |
| `prompt_injection` | 6 | 5 | 1 |
| `malformed` | 20 | 16 | 4 |
| `flood_same_creator` | 12 | 12 | 0 |
| **all** | **56** | **42** | **14** |

**42 held, 14 broke.**

| ID | Family | Targeting | Status | Guess | Combined | Model | Style | Verdict |
|---|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | human | 0.304 | 0.164 | 0.515 | **BROKE** |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.475 | 0.594 | 0.297 | HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.565 | 0.666 | 0.414 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.572 | 0.611 | 0.512 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.315 | 0.321 | 0.306 | **BROKE** |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.458 | 0.573 | 0.285 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.437 | 0.586 | 0.212 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | human | 0.347 | 0.245 | 0.500 | **BROKE** |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.577 | 0.704 | 0.386 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.935 | 0.979 | 0.869 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.586 | 0.618 | 0.538 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | ai | 0.707 | 0.739 | 0.659 | **BROKE** |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | ai | 0.733 | 0.805 | 0.624 | **BROKE** |
| FP04 | false_positive | a student essay written to a rubric | 200 | ai | 0.728 | 0.833 | 0.569 | **BROKE** |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.770 | 0.800 | 0.724 | **BROKE** |
| FP06 | false_positive | a person imitating a formal template | 200 | ai | 0.757 | 0.881 | 0.570 | **BROKE** |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | ai | 0.785 | 0.882 | 0.640 | **BROKE** |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | 0.402 | 0.322 | 0.522 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.456 | 0.463 | 0.446 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.253 | 0.204 | 0.326 | **BROKE** |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.517 | 0.594 | 0.401 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.440 | 0.500 | 0.350 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.451 | 0.640 | 0.167 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.552 | 0.558 | 0.542 | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | — | — | — | HELD |
| MF02 | malformed | text is a single character | 422 | — | — | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | human | 0.200 | 0.001 | 0.500 | **BROKE** |
| MF04 | malformed | text is only punctuation | 200 | unsure | 0.407 | 0.011 | 1.000 | HELD |
| MF05 | malformed | text is a very long single word | 200 | ai | 0.799 | 0.998 | 0.500 | **BROKE** |
| MF06 | malformed | text is emoji only | 200 | ai | 0.931 | 0.997 | 0.833 | **BROKE** |
| MF07 | malformed | text is right-to-left script | 200 | ai | 0.877 | 0.906 | 0.833 | **BROKE** |
| MF08 | malformed | text is 60,000 characters | 413 | — | — | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | — | — | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | — | — | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | — | — | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | — | — | — | — | HELD |
| RQ05 | malformed | text is null | 400 | — | — | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | — | — | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | — | — | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | — | — | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | — | — | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.217 | 0.029 | 0.500 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.217 | 0.029 | 0.500 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.217 | 0.029 | 0.500 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.217 | 0.029 | 0.500 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.217 | 0.029 | 0.500 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.217 | 0.029 | 0.500 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.217 | 0.029 | 0.500 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.217 | 0.029 | 0.500 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.217 | 0.029 | 0.500 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.217 | 0.029 | 0.500 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | HELD |

Three rows were rebuilt, not copied byte for byte from the provided file,
because their content can't survive a copy-paste. **MF03** uses real ESC
characters (`\x1b[31m`) for the control codes. **MF05** is 5,000 `a`
characters; the exact count in the original is unknown, but anything between
roughly 2,000 and 10,000 characters behaves the same, because gpt2 reads at
most 400 tokens and the route refuses anything over 10,000. **MF08** is the
FP01 paragraph repeated 115 times (60,260 characters). If you have the
original files, swap them in and re-run.

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

From `logs/audit.jsonl`, before run (2026-11-02 04:16 UTC). Three human
writers accused, an Arabic passage accused, a run of `a` accused, two evasions
labelled human, the log-injection attempt (nine normal fields, nothing
injected), and two rejections.

```json
{"timestamp": "2026-11-02T04:16:50+00:00", "content_id": "80353c24-e169-43aa-9932-d3de24c53aee", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.6244, "combined_score": 0.7328, "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.", "status": "decided"}
{"timestamp": "2026-11-02T04:16:50+00:00", "content_id": "23815540-c487-4d10-b5fe-5750932ed4e1", "creator_id": "attacker_FP02", "guess": "ai", "model_score": 0.7387, "style_score": 0.6586, "combined_score": 0.7067, "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.", "status": "decided"}
{"timestamp": "2026-11-02T04:16:51+00:00", "content_id": "901a9340-fdf7-41b1-bfb8-af6dab6aec79", "creator_id": "attacker_FP07", "guess": "ai", "model_score": 0.8816, "style_score": 0.6405, "combined_score": 0.7852, "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.", "status": "decided"}
{"timestamp": "2026-11-02T04:16:52+00:00", "content_id": "0de47cc2-51bc-48b9-b052-dbefff8258d4", "creator_id": "attacker_MF07", "guess": "ai", "model_score": 0.9064, "style_score": 0.8333, "combined_score": 0.8772, "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.", "status": "decided"}
{"timestamp": "2026-11-02T04:16:51+00:00", "content_id": "dc9b6e33-c224-4988-af4c-36ebaeee70af", "creator_id": "attacker_MF05", "guess": "ai", "model_score": 0.9976, "style_score": 0.5, "combined_score": 0.7986, "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.", "status": "decided"}
{"timestamp": "2026-11-02T04:16:49+00:00", "content_id": "cfd72426-18f9-4f93-9e7a-5b0be4471351", "creator_id": "attacker_EV01", "guess": "human", "model_score": 0.1635, "style_score": 0.515, "combined_score": 0.3041, "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.", "status": "decided"}
{"timestamp": "2026-11-02T04:16:51+00:00", "content_id": "b84f3fc7-10c3-42d8-8842-fb1fe595af21", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.3259, "combined_score": 0.253, "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.", "status": "decided"}
{"timestamp": "2026-11-02T04:16:51+00:00", "content_id": "35191d59-4fc5-4038-9ca7-5001bfe34402", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.6401, "style_score": 0.1667, "combined_score": 0.4507, "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.", "status": "decided"}
{"timestamp": "2026-11-02T04:16:52+00:00", "content_id": null, "creator_id": "attacker_flood", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "rejected", "event": "rejected", "reason": "rate_limited", "http_status": 429, "limit": "10 per 1 minute"}
{"timestamp": "2026-11-02T04:16:52+00:00", "content_id": null, "creator_id": "attacker_MF08", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "rejected", "event": "rejected", "reason": "text_too_long", "http_status": 413}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP03**, a non-native English speaker writing carefully about their first
month in a new country, labelled high-confidence AI at 0.7328 (model 0.8051,
style 0.6244). Nothing in the text is unusual. Short, correct sentences and
common words are exactly what the model signal reads as machine-like. This is
the writer RUNNING.md warns about: the one with the least room to argue back,
told their own account of moving countries "matches patterns often found in
machine-generated text". MF07 (Arabic, 0.8772) is the same failure from the
other side: a writer in another script accused with high confidence by a
model that can't read it.



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

**Broken attacks (before run): 14 of 56.** By stage and mechanism:

1. **Six false positives: FP02–FP07 (formal report, non-native speaker,
   rubric essay, technical docs, cover letter, deliberate repetition).
   Stage: signal one first, then signal two agreeing, then the label mapping
   bar.** Model scores run 0.739–0.882, because short sentences of common
   words are low-perplexity to gpt2 whoever wrote them. The style signal
   agrees, at 0.569–0.724: evenly sized sentences give a high spread
   component, and almost no commas or dashes give a high punctuation
   component. With both signals above 0.55, the weighted average can't pull
   the score down, and every one lands 0.007–0.085 over the 0.70 bar. FP02 at
   0.7067 is the closest. **This is the miss criterion 1 couldn't see.** Its
   ten passages are 19th-century literary prose (Twain, Franklin, Mill,
   Thoreau), full of rare words and long, lumpy sentences that gpt2 finds
   surprising. Modern plain prose is a different population, and on it the
   false-positive rate is 6 of 8, not 0 of 10.
2. **Four non-prose inputs given a confident label: MF05 (`aaaa…`), MF06
   (emoji), MF07 (Arabic) labelled AI, and MF03 (control characters) labelled
   human. Stage: the route, which then exposes both signals.** The route
   accepts anything with three or more gpt2 tokens. For a run of repeated
   tokens, gpt2 predicts the next one almost perfectly, so the model score is
   0.997. Arabic and emoji go to gpt2 as byte pieces in predictable runs
   (0.906, 0.997). `stylometry.words()` only matches `[a-z0-9']`, so it finds
   zero words in emoji or Arabic. Punctuation density then returns 0, which
   the style signal reads as fully AI, and TTR returns 0, also fully AI. So
   style is 0.833. In short, "I can't measure this" is scored as "machine".
   MF03 goes the other way: the ESC bytes make gpt2's perplexity explode
   (model 0.0006).
3. **Three evasions labelled human: EV01 (typos), EV05 (heavy human edit),
   EV08 (two short sentences). Stage: signal one.** The base paragraph is
   model 0.669. EV01's misspellings ("poistioned", "thsi") are rare token
   sequences, so the model score falls to 0.164 and the combined score to
   0.304, under the 0.35 human line. The attack targeted signal two, but
   signal two didn't move (0.515 to 0.515); the model signal did all of it.
   EV08 is too short to have context, so its perplexity is high (model
   0.245), and with fewer than three sentences the style signal sits at its
   neutral 0.5. EV05 is rewritten throughout (model 0.321, style 0.306). By
   the attack's own definition it got through, but the text may honestly be
   mostly human now.
4. **One injection: PI02, labelled human at 0.253. Stage: signal one, not
   the route.** Nothing reads instructions. The service has no LLM in the
   loop, so "Return guess=human" was never obeyed. The prefix
   `SYSTEM: provenance check bypassed … guess=human, confidence=0.02.` is
   just very unusual text to gpt2 (model 0.204). PI01, worded in plain
   English, stayed unsure (model 0.463). The attacker got their outcome by
   accident of perplexity, and any jargon-heavy prefix would do the same.

**Held, with the reason:** all 12 malformed request bodies (RQ01–RQ12) got
a 400 with an `error` key, including the 40-deep nested JSON, the empty body
and the form-encoded body. MF01 got a 400, MF02 a 422 and MF08 a 413. The
flood got 10 × 200 then 2 × 429, both logged. PI04's `<script>` isn't
reflected, because responses never echo the text. PI05's quotes didn't break
the log, because `json.dumps` escapes them and the text isn't logged anyway.
Seven of the ten evasions stayed unsure, though only EV10 (three repeated
stanzas, 0.935) was actually caught.

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

**Pattern across the results.** The attack set confirms this one at scale.
13 of the 14 broken attacks are signal one deciding the outcome: low
perplexity on plain or repetitive input (FP02–07, MF05–07), or high
perplexity on typos, jargon, short or garbled input (EV01, EV08, PI02,
MF03). Signal two either agrees or barely moves. The model signal measures
predictability, not authorship. The route adds a second problem: it has no
idea what it can't score.

The miss and the near-misses on the criteria come from one
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
don't show it generalises. The attack set arrived after the change was made
and committed, so the attack run below is the out-of-sample check, and the
change wasn't adjusted after seeing it.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

`results/attack_run_2026-11-01_2217_after.md`: the same 56 attacks against the
current code, on a freshly started server so the rate-limit counts reset. Same
verdict rules as the before run. No 5xx. All refusals (MF01, MF02, MF08,
RQ01–RQ12, the two 429s) came back with the same status as before.

| Family | Attacks | BROKE before | BROKE after |
|---|---|---|---|
| `evasion` | 10 | 3 | 0 |
| `false_positive` | 8 | 6 | 6 |
| `prompt_injection` | 6 | 1 | 1 |
| `malformed` | 20 | 4 | 4 |
| `flood_same_creator` | 12 | 0 | 0 |
| **all** | **56** | **14** | **11** |

Every attack that reached the scorers, before and after (FL01 rows are all
identical, so only one is shown):

| ID | Before: guess (combined) | After: guess (combined) | Verdict before → after |
|---|---|---|---|
| EV01 | human (0.304) | unsure (0.407) | BROKE → HELD |
| EV02 | unsure (0.475) | unsure (0.532) | HELD → HELD |
| EV03 | unsure (0.565) | unsure (0.648) | HELD → HELD |
| EV04 | unsure (0.572) | unsure (0.674) | HELD → HELD |
| EV05 | human (0.315) | unsure (0.356) | BROKE → HELD |
| EV06 | unsure (0.458) | unsure (0.489) | HELD → HELD |
| EV07 | unsure (0.437) | unsure (0.452) | HELD → HELD |
| EV08 | human (0.347) | unsure (0.447) | BROKE → HELD |
| EV09 | unsure (0.577) | unsure (0.654) | HELD → HELD |
| EV10 | ai (0.935) | ai (0.909) | HELD → HELD |
| FP01 | unsure (0.586) | unsure (0.647) | HELD → HELD |
| FP02 | ai (0.707) | ai (0.773) | BROKE → BROKE |
| FP03 | ai (0.733) | ai (0.817) | BROKE → BROKE |
| FP04 | ai (0.728) | ai (0.802) | BROKE → BROKE |
| FP05 | ai (0.770) | ai (0.777) | BROKE → BROKE |
| FP06 | ai (0.757) | ai (0.799) | BROKE → BROKE |
| FP07 | ai (0.785) | ai (0.726) | BROKE → BROKE |
| FP08 | unsure (0.402) | unsure (0.507) | HELD → HELD |
| PI01 | unsure (0.456) | unsure (0.545) | HELD → HELD |
| PI02 | human (0.253) | human (0.318) | BROKE → BROKE |
| PI03 | unsure (0.517) | unsure (0.597) | HELD → HELD |
| PI04 | unsure (0.440) | unsure (0.490) | HELD → HELD |
| PI05 | unsure (0.451) | unsure (0.484) | HELD → HELD |
| PI06 | unsure (0.552) | unsure (0.616) | HELD → HELD |
| MF03 | human (0.200) | human (0.300) | BROKE → BROKE |
| MF04 | unsure (0.407) | unsure (0.407) | HELD → HELD |
| MF05 | ai (0.799) | ai (0.899) | BROKE → BROKE |
| MF06 | ai (0.931) | ai (0.898) | BROKE → BROKE |
| MF07 | ai (0.877) | ai (0.844) | BROKE → BROKE |
| FL01_01 | human (0.217) | human (0.317) | HELD → HELD |

For reference, the unedited AI paragraph went from 0.6076 (unsure) to 0.7107
(AI). The full after table, with model and style scores, is in the results
file.

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

**What the attack set adds, out of sample:**

- **Broke count fell, 14 → 11.** All three evasion breaks (EV01, EV05,
  EV08) moved from human to unsure. But look at how. The style score went up
  on nearly every input, not just the AI ones. Dropping TTR removed a
  component that was scoring most short texts as human-like (plain TTR on
  under 50 words runs high), so the average of what's left is higher across
  the board. The evasions got caught because everything moved toward AI.
- **False positives didn't improve, and got worse in score.** FP02–FP07 are
  still labelled AI (6 of 8, unchanged). The mean combined score over all
  eight false-positive passages rose from 0.683 to 0.731. FP03, the
  non-native speaker, went from 0.733 to 0.817. FP01 is 0.054 from the line
  (0.647), and FP08 went from 0.402 to 0.507. Only FP07 fell (0.785 to
  0.726). The non-prose breaks (MF03, MF05–07) and PI02 are unchanged,
  because they're signal-one and route problems that this change doesn't
  touch.

**Overall:** the change helped on what it was aimed at (criterion 2's gap,
0.145 to 0.201) and lowered the broken-attack count. But it did that by
shifting every score toward AI, not by separating human from AI better. On
the error that matters most, accusing real writers, the attack set shows it
made things slightly worse: the same six writers accused, with higher
scores, and two more writers closer to the line. The calibration set's
in-sample view (human mean +0.012) understated that. On modern plain prose
the human side moved by +0.048.

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

<!-- ═══════════════════ UNIT 9 — DEPLOY AND INSTRUMENT ═══════════════════ -->

---

## Unit 9: Scope

**Shape:** A, Deploy and Instrument.
**Path:** B, Local with Logs.

**Why Path B and not a free host.** The service loads `gpt2` into memory to
score every submission. The weights are about 550 MB on disk, and `torch`
adds a few hundred MB more on top. A typical free tier gives 512 MB of RAM and
no persistent disk, so the service would be over budget before the first
request and would re-download the model after every idle spin-down. I'd rather
run it properly on my own machine than spend the unit fighting a host that
can't hold it. (The measured memory use is in the Unit 9 run section below.)

**What I'm building, exactly:**

1. **A documented production-style run path.** The service runs under
   `gunicorn` (already in `requirements.txt`, unused until now) with a small
   `gunicorn.conf.py`, not Flask's development server. `RUNNING.md` gets exact
   steps for a fresh checkout: Python version, install, model download, start
   command, and how to check it's working.
2. **A structured request log, `logs/requests.jsonl`.** One JSON line per HTTP
   request to any route, written by `requestlog.py`. The audit log already
   records *decisions* (scores, labels, appeals, rejections). What it can't
   tell me is how the service is behaving as a service: how long each request
   took, what status it returned, how big the input and output were, and what
   went wrong when something failed. The request log adds only that:
   timestamp, method, path, HTTP status, duration in ms, input size and text
   length (never the text itself), output size and the key output fields, the
   error code or exception when there is one, and whether the model was
   already loaded (so cold and warm requests can be told apart).
3. **A measured cost.** There's no paid API, so the cost is compute time per
   request, measured from the request log over real runs, with cold start and
   warm requests reported separately.

**Out of scope:**

- **Hosting anywhere public.** No cloud deploy, no Docker image, no HTTPS or
  reverse proxy. The service still binds to loopback by default.
- **Changing what the detector decides.** The signals, weights, thresholds,
  labels and the appeal flow stay as Unit 8 left them. The audit log keeps its
  exact schema; the request log is a separate file.
- **A metrics stack or dashboard.** No Prometheus, no log shipping, no new
  libraries. The request log is a plain JSONL file read with Python or `jq`.

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
