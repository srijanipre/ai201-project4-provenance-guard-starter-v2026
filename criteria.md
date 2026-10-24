# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---

## 1. False positives stay rare on human writing

Of 10 passages I know were written by people (5 plain, 5 formal; all from
public-domain books published before 2020, so no chance of model output), at
most **1 of 10** gets the high-confidence AI label. Checked in each of three
runs, and every run has to hold.

**Why this target:** A wrong accusation is the expensive error here. A writer
who gets told their essay was probably machine-written has to prove a negative,
and the system can't help them. Missing some AI text costs the site very
little by comparison. 10% is still generous for a system this blunt, and I
picked it knowing the gpt2 signal is likely to hit plain writing hardest.

---

## 2. Clearly AI and clearly human text separate

Mean combined score of 5 clearly AI passages minus mean combined score of the
10 human passages from criterion 1 must be **at least 0.30**. The AI passages
are ones I wrote in a generic assistant voice, so their origin is known by
construction, not verified from outside.

**Why this target:** If the two groups barely separate, no threshold I pick is
going to tell them apart, and the labels are just noise with extra steps. 0.30
is about the width of the unsure band I'm planning, so a gap that small would
mean the middle band is covering the whole space.

---

## 3. All three labels are reachable

Two checks. First, real submissions from the eval set produce **all three**
labels (high-confidence AI, high-confidence human, unsure) at least once. Second,
`scoring.score_to_label` returns the expected label at each boundary: 0.00,
just under and at `HUMAN_THRESHOLD`, just over and at `AI_THRESHOLD`, and 1.00.
That's **7 of 7** boundary checks passing.

**Why this target:** A label nobody can reach is dead text in the README, and
a gap between ranges would mean some score gets no label at all. Testing the
exact boundaries catches off-by-one mistakes (`>` vs `>=`) that a random sample
would miss.

---

## 4. Appeals always change status and always get logged

For 5 submissions covering at least two different labels, `POST /appeal`
returns 200 with `"status": "under_review"`, and the log gains exactly one
`appeal` entry with the same `content_id`. The original decision entry for each
ID is still in the log and unchanged. An appeal on a made-up `content_id`
returns 404 and adds zero lines to the log. A second appeal on the same ID
returns 409. That's **5 of 5** appeals and **3 of 3** error cases.

**Why this target:** The appeal path is the only recourse a writer has, since
nothing gets re-scored automatically. If an appeal can silently fail, or
overwrite the original decision, the record of what happened is gone, and
that's the record anyone reviewing the case would need.

---

## 5. Malformed input is refused cleanly

Eight malformed requests: empty `text`, whitespace-only `text`, missing `text`,
`text` set to `null`, `text` as a number, missing `creator_id`, `text` over
10,000 characters, and a body that isn't JSON. Every one must return a 4xx
status with a JSON body that has an `error` key, and **none** may return a 5xx.
None of them may add a decision entry to the audit log. That's **8 of 8**.

**Why this target:** A crash on bad input is one of the most common real
failures, and a 500 tells the caller nothing. Writing a decision entry for a
request that never got scored would also muddy the log, which is supposed to
show only real decisions.

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
