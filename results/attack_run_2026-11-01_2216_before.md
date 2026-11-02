# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-01 22:16
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `cfd72426-18f9-4f93-9e7a-5b0be4471351` | human | 0.304 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `ea2443c3-72f1-4426-b260-9041b2cef6da` | unsure | 0.475 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `12b9c27f-7fea-4c84-92a9-fe054486e4ad` | unsure | 0.565 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `bfdb8c79-9d8e-4efd-a489-e9ca88f240d6` | unsure | 0.572 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `296f39b9-b7ab-477d-988a-acff805330af` | human | 0.315 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `2ae7dca6-faaf-4741-8915-e8e8546c02cb` | unsure | 0.458 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `220a9727-d7ea-49d9-b3f9-d7a9328fcff8` | unsure | 0.437 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `7c0627b2-56ab-4639-bdf2-dda8bf176d6f` | human | 0.347 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `4a45d721-1a8b-4bfa-8532-806e89703ddf` | unsure | 0.577 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `1e6edd6e-2709-4a97-a41b-6179443b705d` | ai | 0.935 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `32947b94-5b80-4158-a0bd-2bbb0c49d2f4` | unsure | 0.586 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `23815540-c487-4d10-b5fe-5750932ed4e1` | ai | 0.707 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `80353c24-e169-43aa-9932-d3de24c53aee` | ai | 0.733 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `f05e71b4-9524-40e3-9e73-d9c16054c3df` | ai | 0.728 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `984eeff3-a419-47fa-9b2b-7f78e274d4df` | ai | 0.770 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `aff08a7b-cba5-4aca-8f6c-8552c821a31e` | ai | 0.757 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `901a9340-fdf7-41b1-bfb8-af6dab6aec79` | ai | 0.785 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `801459f1-54fd-49cb-994b-1182563315d9` | unsure | 0.402 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `b30d71bf-6fdb-493f-a5e3-9d6f9666f7a9` | unsure | 0.456 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `b84f3fc7-10c3-42d8-8842-fb1fe595af21` | human | 0.253 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c864326a-3e20-4b8f-8849-aaf20ef028bc` | unsure | 0.517 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `5b7e3208-36d5-4452-bdb9-6bf51831651e` | unsure | 0.440 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `35191d59-4fc5-4038-9ca7-5001bfe34402` | unsure | 0.451 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `092d2f31-c887-4ea8-8635-7aeb8a41eeed` | unsure | 0.552 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 422 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `6687f58c-2cb6-49a0-93e8-f4d80e0e6f87` | human | 0.200 |  |
| MF04 | malformed | text is only punctuation | 200 | `423d08d7-3815-468d-a217-c57a58336301` | unsure | 0.407 |  |
| MF05 | malformed | text is a very long single word | 200 | `dc9b6e33-c224-4988-af4c-36ebaeee70af` | ai | 0.799 |  |
| MF06 | malformed | text is emoji only | 200 | `9e0a3638-ae15-4761-b29b-e0a48bec52f5` | ai | 0.931 |  |
| MF07 | malformed | text is right-to-left script | 200 | `0de47cc2-51bc-48b9-b052-dbefff8258d4` | ai | 0.877 |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `10e3ae6e-b2e5-44f8-818e-1f23226b5c7e` | human | 0.217 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `50d02d94-cf5a-42dc-89c5-75bace94de45` | human | 0.217 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `10561925-d3bc-4684-bde5-8646f3a50aac` | human | 0.217 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `437436cb-61bb-46c5-b61f-c8aef9d2ba6b` | human | 0.217 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f5136b85-ac6a-42b6-9c8f-68d293856ba8` | human | 0.217 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `644a575d-b85f-42aa-b7bb-5a5e39f4f043` | human | 0.217 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b8401f90-e1a2-4dfb-a32e-343b8264038c` | human | 0.217 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0ee5b8f0-bc97-47e2-91f5-284798fe4820` | human | 0.217 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `645b0ff9-75c6-41af-9101-7d12e143b92a` | human | 0.217 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `07825937-51db-4fdf-9d6c-c4d51c5652e2` | human | 0.217 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "cfd72426-18f9-4f93-9e7a-5b0be4471351",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.3041,
  "model_score": 0.1635,
  "style_score": 0.515,
  "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "ea2443c3-72f1-4426-b260-9041b2cef6da",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4753,
  "model_score": 0.5943,
  "style_score": 0.2968,
  "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "12b9c27f-7fea-4c84-92a9-fe054486e4ad",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5654,
  "model_score": 0.6662,
  "style_score": 0.4141,
  "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "bfdb8c79-9d8e-4efd-a489-e9ca88f240d6",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5716,
  "model_score": 0.6114,
  "style_score": 0.5118,
  "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "296f39b9-b7ab-477d-988a-acff805330af",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3151,
  "model_score": 0.3212,
  "style_score": 0.306,
  "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "2ae7dca6-faaf-4741-8915-e8e8546c02cb",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4578,
  "model_score": 0.5727,
  "style_score": 0.2854,
  "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "220a9727-d7ea-49d9-b3f9-d7a9328fcff8",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4366,
  "model_score": 0.5862,
  "style_score": 0.2122,
  "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "7c0627b2-56ab-4639-bdf2-dda8bf176d6f",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.3471,
  "model_score": 0.2452,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "4a45d721-1a8b-4bfa-8532-806e89703ddf",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5768,
  "model_score": 0.7042,
  "style_score": 0.3857,
  "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "1e6edd6e-2709-4a97-a41b-6179443b705d",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.935,
  "model_score": 0.9792,
  "style_score": 0.8687,
  "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "32947b94-5b80-4158-a0bd-2bbb0c49d2f4",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5858,
  "model_score": 0.6175,
  "style_score": 0.5383,
  "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "23815540-c487-4d10-b5fe-5750932ed4e1",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7067,
  "model_score": 0.7387,
  "style_score": 0.6586,
  "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "80353c24-e169-43aa-9932-d3de24c53aee",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7328,
  "model_score": 0.8051,
  "style_score": 0.6244,
  "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "f05e71b4-9524-40e3-9e73-d9c16054c3df",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7275,
  "model_score": 0.8329,
  "style_score": 0.5694,
  "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "984eeff3-a419-47fa-9b2b-7f78e274d4df",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7697,
  "model_score": 0.8005,
  "style_score": 0.7236,
  "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "aff08a7b-cba5-4aca-8f6c-8552c821a31e",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.7569,
  "model_score": 0.8814,
  "style_score": 0.5702,
  "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "901a9340-fdf7-41b1-bfb8-af6dab6aec79",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7852,
  "model_score": 0.8816,
  "style_score": 0.6405,
  "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "801459f1-54fd-49cb-994b-1182563315d9",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.4023,
  "model_score": 0.3223,
  "style_score": 0.5223,
  "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "b30d71bf-6fdb-493f-a5e3-9d6f9666f7a9",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4558,
  "model_score": 0.4625,
  "style_score": 0.4458,
  "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "b84f3fc7-10c3-42d8-8842-fb1fe595af21",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.253,
  "model_score": 0.2044,
  "style_score": 0.3259,
  "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "c864326a-3e20-4b8f-8849-aaf20ef028bc",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5169,
  "model_score": 0.5943,
  "style_score": 0.4008,
  "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "5b7e3208-36d5-4452-bdb9-6bf51831651e",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4398,
  "model_score": 0.4998,
  "style_score": 0.3499,
  "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "35191d59-4fc5-4038-9ca7-5001bfe34402",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4507,
  "model_score": 0.6401,
  "style_score": 0.1667,
  "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "092d2f31-c887-4ea8-8635-7aeb8a41eeed",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5517,
  "model_score": 0.5583,
  "style_score": 0.5419,
  "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "6687f58c-2cb6-49a0-93e8-f4d80e0e6f87",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.2004,
  "model_score": 0.0006,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "423d08d7-3815-468d-a217-c57a58336301",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.4067,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "dc9b6e33-c224-4988-af4c-36ebaeee70af",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.7986,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "9e0a3638-ae15-4761-b29b-e0a48bec52f5",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9315,
  "model_score": 0.9969,
  "style_score": 0.8333,
  "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "0de47cc2-51bc-48b9-b052-dbefff8258d4",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.8772,
  "model_score": 0.9064,
  "style_score": 0.8333,
  "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "10e3ae6e-b2e5-44f8-818e-1f23226b5c7e",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2172,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "50d02d94-cf5a-42dc-89c5-75bace94de45",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2172,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "10561925-d3bc-4684-bde5-8646f3a50aac",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2172,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "437436cb-61bb-46c5-b61f-c8aef9d2ba6b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2172,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "f5136b85-ac6a-42b6-9c8f-68d293856ba8",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2172,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "644a575d-b85f-42aa-b7bb-5a5e39f4f043",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2172,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "b8401f90-e1a2-4dfb-a32e-343b8264038c",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2172,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "0ee5b8f0-bc97-47e2-91f5-284798fe4820",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2172,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "645b0ff9-75c6-41af-9101-7d12e143b92a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2172,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "07825937-51db-4fdf-9d6c-c4d51c5652e2",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2172,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
