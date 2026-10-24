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
