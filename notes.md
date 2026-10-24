# Provenance Guard — dev notes

Working notes for the build. Milestone 1 (the trace and the signal analysis)
lives here, and so do the stylometry and scoring decisions and the calibration
numbers from later milestones.

---

## Milestone 1 — the submission flow

Going through the starter in the order I'll actually build it:

1. **Receive the request.** Flask gets `POST /submit` with a JSON body. Nothing
   is parsed until the route runs, so `request.get_json(silent=True)` is the
   first thing that can go wrong: a body that isn't JSON comes back as `None`.
2. **Validate.** Body has to be a dict. `text` has to be present, a string, not
   whitespace-only, and under `MAX_TEXT_CHARS`. `creator_id` has to be a
   non-empty string. Anything else gets a 4xx JSON error and nothing is logged
   as a decision.
3. **Signal one (semantic / model).** `detector.model_signal(text)` runs gpt2
   locally, gets perplexity, and squashes it to 0–1 with higher = more AI. The
   model is loaded once and kept in `detector._model`. If the text is under
   three tokens, `perplexity()` raises `ValueError` and the route turns that
   into a 422.
4. **Signal two (style).** `stylometry.style_signal(text)` computes three
   shape measures and returns 0–1, higher = more AI. It doesn't touch the
   model.
5. **Combine.** `scoring.combine_signals(model_score, style_score)` gives one
   0–1 number with the same direction.
6. **Label.** `scoring.score_to_label(combined)` returns `(guess, label_text)`
   from the thresholds in `config.py`.
7. **Log and respond.** `audit.log_decision(...)` appends one JSON line to
   `logs/audit.jsonl` with the ID, creator, all three scores, the guess, the
   label and status `decided`. The route returns the same content as JSON,
   including both signal scores.

Appeals go through `POST /appeal`: check the ID exists in the log, append an
`appeal` event with status `under_review` (the original entry stays where it
is), return JSON.

---

## Milestone 1 — the two signals

### Signal one — the model signal (`detector.py`)

It measures **perplexity**: how surprised gpt2 is by the text, averaged per
token. Low perplexity means the text was easy to predict, and the idea is that
machine text is easy to predict because it's built out of likely next words.
Human writing is supposed to be less predictable, with odd word choices and
sudden turns.

Why that might differ: a model generates by picking high-probability tokens, so
its output sits in the high-probability part of the distribution, which is
exactly what gpt2 finds unsurprising.

Limitations I can see:

- It's predictability, not authorship. Plain writing with common words and
  short sentences is easy for gpt2 to predict, so it scores as AI-ish.
  Someone writing in a second language, a younger writer, or anyone writing
  plainly on purpose would get hit.
- Dense, ornate prose with rare words is the other way around. It's hard for
  gpt2, so it can read as human even when a model wrote it.
- It only sees the first 400 tokens (`DETECTOR_MAX_TOKENS`). A long submission
  gets judged on its opening paragraphs.
- Perplexity depends on topic and length, so the raw number isn't comparable
  across very different texts. The logistic squash with midpoint 45 is a
  choice, not a fact about the world.
- gpt2 is old. Modern models write text that gpt2 may find quite surprising,
  so the signal may be weaker on current AI output than on older output.

False positive it could produce: a plainly written human paragraph with short
sentences and everyday words. Perplexity comes out low, the model score goes
high, and nothing in this signal can push back.

### Signal two — the style signal (`stylometry.py`)

It measures the shape of the text, not its meaning. I'm using three measures:

- **Sentence-length spread.** Coefficient of variation of sentence length in
  words (stdev / mean). Human writing tends to be lumpy, so a higher CV
  reads as more human. Low spread goes toward AI.
- **Type-token ratio (moving-average version).** Unique words over total words,
  computed in windows of 50 words and averaged. The plain ratio falls as the
  text gets longer, so the moving average keeps long and short submissions
  comparable. Higher means more varied vocabulary, which reads as human.
- **Punctuation density.** Commas, semicolons, colons, dashes, and brackets
  per word. Clause-heavy writing with asides and dashes is more typical of
  people, and flat sentences with few marks go toward AI.

Blind spots:

- It can't read. Typos, broken sentences, or a pasted quotation all move the
  numbers without changing what the text says. That's cheap to do on purpose.
- Plain human writing has low sentence variety too, so it can look
  machine-flat on all three measures at once.
- Formal, carefully edited human prose has a lot of punctuation and a varied
  vocabulary, so it reads as human on this signal even when it's a model's
  output that was then tidied up.
- Very short inputs don't give the measures enough to work with. A one-sentence
  submission has no spread at all, so it gets a neutral component value
  instead of a fake reading.

---

## Milestone 1 — the false-positive scenario

A writer submits a short essay written entirely by hand. Plain sentences, a
lot of "the" and "and", no punctuation tricks. Here's how it moves through:

- **Signal one.** gpt2 finds it predictable. Perplexity comes in low, maybe in
  the 20s, so the squashed model score is high, around 0.8.
- **Signal two.** Sentence lengths are close together and there's little
  punctuation. The style score comes out high too, around 0.6–0.7.
- **Combined.** Both signals point the same way, so the combined score is high,
  and the label rule decides what the writer sees. If the AI threshold is
  low, that's a high-confidence AI label on a human essay.
- **What the writer sees.** A label saying the text was probably machine
  written. That's a serious thing to tell someone, and they'd have no idea why
  it happened.
- **Thresholds.** The cost of this error is much higher than the cost of
  letting some AI text through, so the AI threshold has to be high enough that
  two plain-writing signals agreeing still isn't enough on their own, and the
  unsure band should catch the middle.
- **Recourse.** The writer calls `POST /appeal` with their reasoning. The
  status moves to `under_review`, the original decision stays in the log, and
  a person can look at it. No automatic reclassification, so the appeal is the
  only way back, which is why the appeal path has its own criterion.

---

## Milestone 1 — endpoint contracts

### `POST /submit`

Request:

```json
{"text": "some writing", "creator_id": "writer123"}
```

Success (200):

```json
{
  "content_id": "3f2a…",
  "guess": "ai | human | unsure",
  "confidence": 0.0,
  "label": "reader-facing sentence",
  "model_score": 0.0,
  "style_score": 0.0,
  "status": "decided"
}
```

`confidence` is the combined AI-likelihood score, 0–1. It's a score, not a
calibrated probability of authorship.

Errors (all JSON with an `error` key):

| Case | Status | `error` |
|---|---|---|
| Body isn't JSON or isn't an object | 400 | `invalid_body` |
| `text` missing | 400 | `missing_field` |
| `text` not a string, or `creator_id` not a string | 400 | `invalid_type` |
| `text` empty or whitespace-only | 400 | `empty_text` |
| `creator_id` missing or empty | 400 | `missing_field` / `empty_creator_id` |
| `text` over `MAX_TEXT_CHARS` | 413 | `text_too_long` |
| Too short for the detector (< 3 tokens) | 422 | `text_too_short` |
| Detector can't load | 503 | `detector_unavailable` |

### `POST /appeal`

Request:

```json
{"content_id": "3f2a…", "reasoning": "I wrote this myself, here's my draft history."}
```

Success (200):

```json
{
  "content_id": "3f2a…",
  "status": "under_review",
  "original_guess": "ai",
  "message": "..."
}
```

Errors: missing or non-string fields → 400; `content_id` not in the log → 404
`content_not_found`; an appeal already on file → 409 `already_under_review`.
A 404 writes nothing to the log.

---

## Milestone 3 — the submit route

- Started from a hardcoded response and curled it before adding any logic. `/ping` answered the whole time.
- Then validation, then `detector.model_signal`, then `audit.log_decision`.
- Check results (live service, `python app.py`):
  - `{"text": "The implementation of the proposed framework ...", ...}` → 200, real model score.
  - Plain sentences `"I went to the store today. It was raining. I bought milk and bread."` → 200, model score 0.716. The detector reads plain writing as fairly AI-ish, which is the blind spot from Milestone 1.
  - Bad inputs (not JSON, list body, missing text, empty, whitespace, null text, numeric text, missing creator, blank creator, 15,000 characters, two-word text) all return 4xx with an `error` key. None of them writes to the log.
- `GET /health` reports `detector_loaded: true` after the first request. The second request took about 0.06s, so the model is loaded once and reused.
- Detector CLI on one sample from each category (`python detector.py "..."`):

| Category | Sample | Perplexity | model_signal |
|---|---|---|---|
| clearly AI | `ai_clear[0]` | 39.4 | 0.5525 |
| clearly human | `human_plain[0]` (Twain) | 56.5 | 0.4097 |
| borderline | `borderline[0]` (Thoreau) | 79.4 | 0.2873 |

  The separation here is weak. The AI sample lands in the middle. I checked all 15 samples and it's the same picture: some AI text scores under 0.6, and some formal human text scores above 0.7. I didn't move the 45 midpoint to make these look better. Doing that on 15 samples would just be fitting the samples.

---

## Milestone 4 — stylometry and the combining rule

### The calibration set (`samples/calibration.json`)

- **human_plain** (5) and **human_formal** (5): public-domain books published before 2020. Plain is Twain and Franklin, formal is Mill and Thoreau. Source is in each entry.
- **borderline** (1): dense 19th-century Thoreau. Human, but not plain.
- **ai_clear** (5): written by me (Claude) for this set. Origin is known because I wrote them, but it isn't verified from outside.
- **ai_light_edit** (3): hand-edited copies of three `ai_clear` passages, with a few words changed, a contraction, one aside, and sentence rewrites.

Only 15 samples, so every number here is a rough reading and not a real accuracy claim.

### The three style measures (`stylometry.py`)

| Measure | What it computes | Direction | Scale |
|---|---|---|---|
| sentence-length spread | stdev / mean of sentence word counts | higher = more human | `1 - min(cv / 1.0, 1)` |
| type-token ratio | moving-average TTR, 50-word windows | higher = more human | linear 0.5 (AI) to 0.9 (human) |
| punctuation density | `, ; : ( ) — –` per word | higher = more human | `1 - min(rate / 0.12, 1)` |

`style_signal` is the mean of the three AI-ish components. Fewer than three sentences gives a neutral 0.5 spread component. An empty text gives 0.5. The reference points live in `config.py` as `STYLE_*` constants.

Edge cases I checked: empty string, one sentence, repeated word `word word ...`, no punctuation, accented and CJK characters, and 500 repeated words. All return a float in 0–1. Non-ASCII letters get dropped by the starter's `words()` regex, so `café` counts as `caf`. I didn't change that helper.

### What the style measures did on the calibration set

Per-feature gaps, mean AI minus mean human over the 10 human passages:

| Feature | Gap | Reading |
|---|---|---|
| model signal | +0.199 | separates the groups, but formal human text scores high |
| style signal (all three) | +0.065 | weak |
| spread alone | +0.281 | the best single component |
| TTR component | −0.211 | **runs backwards** on this set |
| punctuation component | +0.126 | mild |

The TTR result is the important one. My AI passages have a *higher* moving-average TTR (0.79–0.92) than the human passages (0.69–0.82). The starter's stub says generated prose uses a narrower vocabulary, and that doesn't hold for these samples. I kept the design direction and wrote the reversal down. Flipping it to fit 15 samples would be the kind of fitted result the criteria were written to avoid.

Formal human text also has low sentence spread (CV 0.14–0.46), so it looks machine-flat on that measure. That's the blind spot the Milestone 1 analysis predicted.

### The combining rule (`scoring.py::combine_signals`)

- **Rule:** `combined = (0.6 × model_score + 0.4 × style_score) / (0.6 + 0.4)`, rounded to 4 places and clipped to 0–1. Both inputs are checked to be in 0–1 first.
- **Numbers** (in `config.py`): `WEIGHT_MODEL_SIGNAL = 0.6`, `WEIGHT_STYLE_SIGNAL = 0.4`.
- **Why 0.6 / 0.4:** the model signal separated the groups better on the calibration set (gap 0.20 versus 0.07 for style), and the TTR reversal means the style signal is less trustworthy. I chose this after I'd seen those numbers, so treat it as a judgment call and not as something I validated.
- **Disagreement:** a plain weighted average, so a strong split pulls toward the middle. Example from the calibration set: `ai_clear[1]` has model 0.894 and style 0.504 (a split of 0.39), and combines to 0.738, so the rule did **not** send it to unsure. The model's push won because its weight is higher. A 0.9 vs 0.1 split combines to 0.58 with these weights, which is unsure.

### The rule's output on the calibration set

| Sample | model | style | combined | guess |
|---|---|---|---|---|
| ai_clear[0] | 0.5525 | 0.4393 | 0.5072 | unsure |
| ai_clear[1] | 0.8938 | 0.5043 | 0.7380 | ai |
| ai_clear[2] | 0.7947 | 0.4423 | 0.6537 | unsure |
| ai_clear[3] | 0.5957 | 0.2946 | 0.4753 | unsure |
| ai_clear[4] | 0.7356 | 0.4193 | 0.6091 | unsure |
| human_plain[0] | 0.4097 | 0.2386 | 0.3413 | human |
| human_plain[3] | 0.2541 | 0.2618 | 0.2572 | human |
| human_formal[1] | 0.7481 | 0.3673 | 0.5958 | unsure |

(The full table is in `results/criteria_run_unit7.txt`.)

---

## Milestone 5 — labels and appeals

### Label text and ranges

Ranges are half-open, so every score lands in exactly one label:

| Label | Score range | Reader text |
|---|---|---|
| high-confidence human | below 0.35 | "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee." |
| unsure | 0.35 up to 0.70 | "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result." |
| high-confidence AI | 0.70 and above | "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review." |

- The AI threshold moved from the starter's placeholder 0.65 to 0.70. Formal human passages sit around 0.5 on the combined score, so a higher bar reduces false accusations. That's a trade: most AI text ends up in unsure. Only 1 of the 5 clearly-AI samples reached the AI label.
- `label_ranges()` now prints "below 0.35", "0.35 up to 0.70", and "0.70 and above", so no two ranges overlap at a boundary.

### Appeal path (`app.py::appeal`)

- Validates `content_id` and `reasoning` (non-empty strings, reasoning ≤ 2000 characters).
- 404 `content_not_found` if the ID has no decision entry. Nothing is written.
- 409 `already_under_review` if the last entry for that ID is already `under_review`.
- Otherwise appends an `appeal` event with status `under_review`. The original decision line is untouched.
- The response returns the original guess and label, so the writer can see what they're appealing.
- There's no reclassification. That's on purpose.

### Tests

`python -m unittest discover -s tests -v`: **25 tests, all passing.** They cover stylometry edge cases, weighted combining, bounds and rejection of out-of-range input, threshold boundaries (exact values), that every label is reachable, route validation (all bad bodies, nothing logged), controlled-score label reachability through the route (mocked signals), the full appeal flow, 404 and 409 handling, and that `/ping`, `/health`, `/log` still answer. The route tests write to a temp audit log, not to `logs/audit.jsonl`.

### Scenarios from Milestone 5, Task G

1. Human-written text → `human_plain`, `human_formal` through the live service (criterion run).
2. AI-generated text → `ai_clear` (one reached AI, the rest unsure).
3. Ambiguous text → `borderline` (labelled human, combined 0.29) and the unsure bulk.
4. Invalid input → criterion 5 run, 8 of 8 refused with 4xx.
5. Appeal an existing classification → 5 appeals, 5 of 5 returned 200 with `under_review`.
6. Appeal a nonexistent ID → 404, zero log lines written.
7. Audit history → the appeal entry sits after the original decision for the same ID (see the log tail below).
8. All three labels reachable → real submissions produced `ai` (1), `human` (3), and `unsure` (15). Boundary checks pass too.

---

## Acceptance run against the finished service

The five criteria in `criteria.md` were written before any of this code existed, and I didn't change any targets afterward. The full output is in `results/criteria_run_unit7.txt`.

| # | Criterion | Target | Result | Verdict |
|---|---|---|---|---|
| 1 | False positives on human text | ≤ 1 of 10 labelled AI, all 3 runs | 0 of 10 in all 3 runs | **PASS** |
| 2 | Score separation | mean AI − mean human ≥ 0.30 | 0.145 (mean AI 0.597, mean human 0.451) | **FAIL** |
| 3 | Label coverage | all 3 labels from real text, 6 boundary checks | ai 1, human 3, unsure 15; 6 of 6 boundary checks | **PASS** |
| 4 | Appeal path | 5 of 5 appeals, 3 of 3 error cases | 5 of 5 appeals; 404 wrote 0 lines; 409 on second appeal | **PASS** |
| 5 | Malformed input | 8 of 8 4xx with JSON error, 0 log lines | 8 of 8; 0 log lines | **PASS** |

**Criterion 2 diagnosis:** the model signal alone gives a gap of 0.20, which still misses. The style signal drags it down further. Its TTR component runs backwards on these samples, and formal human text has low sentence spread, so it looks machine-flat. I didn't change the weights or the TTR direction to pass this. It's a real miss, and the fix would need more calibration data and probably a different vocabulary measure, not a retuned constant.

**Criterion 3 note:** the criterion text says "7 of 7" boundary checks, but the procedure it describes names six points (0.00, the two at the human boundary, the two at the AI boundary, and 1.00). I ran those six, and all passed. I'm recording the miscount instead of rewriting the criterion.

---

## Known limitations

- **The detector separates weakly.** Formal human passages reach 0.6–0.75 on the model signal, and the starter's claim that formal prose reads as human doesn't hold for this gpt2 setup.
- **TTR runs backwards** on the calibration set (see above).
- **The detector only reads the first 400 tokens.** A long submission is judged on its opening.
- **Short texts (under 50 words)** fall back to plain TTR, which runs higher than the windowed version, so short submissions lean human on that measure.
- **No auth on appeals.** Anyone with a `content_id` can appeal, and `creator_id` isn't checked.
- **Duplicate-appeal check isn't atomic.** The check reads the log and then appends, with no lock across both. Fine for one process, not for concurrent appeals.
- **`test.py` disk check fails** at 3.5 GB free against its 9 GB guideline. The gpt2 model is already downloaded and runs, so this is the guideline and not a real blocker.
- **The calibration set is small.** 15 samples, with the AI side written by me. The numbers are readings, not accuracy claims.
