# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-01 22:17
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `9695b290-da35-4e7c-88d8-3cb3b00668b0` | unsure | 0.407 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `8ce687f0-3da2-47fd-b682-907f1dd50b3d` | unsure | 0.532 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `ca84dd3b-b233-41e7-bcf3-c9152eee5f8f` | unsure | 0.648 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `6b47e011-0b09-433c-a8c2-92027d804583` | unsure | 0.674 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `dd06eee1-57d2-4ab4-aa7a-a80d79bfae2f` | unsure | 0.356 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `538fb9ba-cdb8-4983-bd90-3280d1a05120` | unsure | 0.489 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `0846613b-f53d-414b-84e5-93b3f133b956` | unsure | 0.452 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `6aa06a1a-a78e-45a8-9551-ce86e76bc682` | unsure | 0.447 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `33761c84-4093-4660-9c97-d60ffec8dced` | unsure | 0.654 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `c141cbdd-6a49-4878-b94b-6a1583b88080` | ai | 0.909 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `004e4f7a-aed3-4718-9ea8-4f475964debe` | unsure | 0.647 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `a0d52051-4355-4011-9c42-19dd31d26d86` | ai | 0.773 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `b367d31c-c402-45a3-bcba-6ee58735155c` | ai | 0.817 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `6dd828bf-f4b3-40c0-9358-e0cbd9f0b694` | ai | 0.802 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `1d4009ef-1be1-476f-bdad-7b919d45af04` | ai | 0.777 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `44a4fd0f-6bd1-4bf8-8f1f-52fd42eab061` | ai | 0.799 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `237b2ebb-8744-442d-a6d5-86b3a2fcf8a0` | ai | 0.726 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `547e6916-da4a-4d6b-adc9-c9ba029920a6` | unsure | 0.507 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `725e3f00-6abb-46c1-8d83-95dba7f44153` | unsure | 0.545 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `58a47a7c-cc83-483c-a9ce-0a2c17a8c268` | human | 0.318 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `15aaf0ea-71d8-477d-8188-9376f18759c8` | unsure | 0.597 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `4c14fe40-a851-489b-83d1-aea9b35db55d` | unsure | 0.490 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `9aa886fc-84a9-40ca-bdd3-57e167d89ca6` | unsure | 0.484 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `fa4d7185-ca6c-4ab9-aaaa-d6e14d4fe589` | unsure | 0.616 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 422 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `8f6e2eb5-6c41-4794-b45d-a50ce64e0986` | human | 0.300 |  |
| MF04 | malformed | text is only punctuation | 200 | `4388dbdc-1d2a-43ae-b1a2-1b48f0fecbba` | unsure | 0.407 |  |
| MF05 | malformed | text is a very long single word | 200 | `e3a32df2-ff80-46d2-8873-b137c1e35a3a` | ai | 0.899 |  |
| MF06 | malformed | text is emoji only | 200 | `d5fead67-3b42-44a0-b10c-e72c7c0572e9` | ai | 0.898 |  |
| MF07 | malformed | text is right-to-left script | 200 | `e6504a4a-17b2-41b7-8039-e29688acd3ab` | ai | 0.844 |  |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `963781e6-375d-4456-b815-17c7a058e5b4` | human | 0.317 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `61fd7778-be83-4292-acec-39fcb7992453` | human | 0.317 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ef9b3a26-0bf6-48d9-833f-b1d4bbc71e4e` | human | 0.317 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `77848998-1e90-45d6-abbb-4b2f0bc710bb` | human | 0.317 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0d729964-160b-4a78-a995-95feeb3e7c45` | human | 0.317 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8166a6d1-6164-49e9-b620-648d70e25e62` | human | 0.317 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a4151932-fd2e-4f90-aa31-dd37f7c0f200` | human | 0.317 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `12d38039-14c0-4d6e-9de4-f8ae10501d08` | human | 0.317 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `6801dc1d-d625-4a52-ad7b-81b3c9c5ae7e` | human | 0.317 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `04700f70-1112-4a3b-8700-d4c7ee9bb287` | human | 0.317 |  |
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
  "content_id": "9695b290-da35-4e7c-88d8-3cb3b00668b0",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4071,
  "model_score": 0.1635,
  "style_score": 0.7726,
  "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
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
  "content_id": "8ce687f0-3da2-47fd-b682-907f1dd50b3d",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5318,
  "model_score": 0.5943,
  "style_score": 0.4381,
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
  "content_id": "ca84dd3b-b233-41e7-bcf3-c9152eee5f8f",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.6482,
  "model_score": 0.6662,
  "style_score": 0.6211,
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
  "content_id": "6b47e011-0b09-433c-a8c2-92027d804583",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6739,
  "model_score": 0.6114,
  "style_score": 0.7676,
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
  "content_id": "dd06eee1-57d2-4ab4-aa7a-a80d79bfae2f",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.356,
  "model_score": 0.3212,
  "style_score": 0.4083,
  "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
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
  "content_id": "538fb9ba-cdb8-4983-bd90-3280d1a05120",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4893,
  "model_score": 0.5727,
  "style_score": 0.3641,
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
  "content_id": "0846613b-f53d-414b-84e5-93b3f133b956",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4517,
  "model_score": 0.5862,
  "style_score": 0.25,
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
  "content_id": "6aa06a1a-a78e-45a8-9551-ce86e76bc682",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.4471,
  "model_score": 0.2452,
  "style_score": 0.75,
  "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
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
  "content_id": "33761c84-4093-4660-9c97-d60ffec8dced",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.6539,
  "model_score": 0.7042,
  "style_score": 0.5785,
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
  "content_id": "c141cbdd-6a49-4878-b94b-6a1583b88080",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.9087,
  "model_score": 0.9792,
  "style_score": 0.803,
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
  "content_id": "004e4f7a-aed3-4718-9ea8-4f475964debe",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.6466,
  "model_score": 0.6175,
  "style_score": 0.6903,
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
  "content_id": "a0d52051-4355-4011-9c42-19dd31d26d86",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7732,
  "model_score": 0.7387,
  "style_score": 0.825,
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
  "content_id": "b367d31c-c402-45a3-bcba-6ee58735155c",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.8174,
  "model_score": 0.8051,
  "style_score": 0.8359,
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
  "content_id": "6dd828bf-f4b3-40c0-9358-e0cbd9f0b694",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.8019,
  "model_score": 0.8329,
  "style_score": 0.7554,
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
  "content_id": "1d4009ef-1be1-476f-bdad-7b919d45af04",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7773,
  "model_score": 0.8005,
  "style_score": 0.7425,
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
  "content_id": "44a4fd0f-6bd1-4bf8-8f1f-52fd42eab061",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.799,
  "model_score": 0.8814,
  "style_score": 0.6753,
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
  "content_id": "237b2ebb-8744-442d-a6d5-86b3a2fcf8a0",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7263,
  "model_score": 0.8816,
  "style_score": 0.4933,
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
  "content_id": "547e6916-da4a-4d6b-adc9-c9ba029920a6",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.5068,
  "model_score": 0.3223,
  "style_score": 0.7835,
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
  "content_id": "725e3f00-6abb-46c1-8d83-95dba7f44153",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.545,
  "model_score": 0.4625,
  "style_score": 0.6687,
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
  "content_id": "58a47a7c-cc83-483c-a9ce-0a2c17a8c268",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.3182,
  "model_score": 0.2044,
  "style_score": 0.4889,
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
  "content_id": "15aaf0ea-71d8-477d-8188-9376f18759c8",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5971,
  "model_score": 0.5943,
  "style_score": 0.6012,
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
  "content_id": "4c14fe40-a851-489b-83d1-aea9b35db55d",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4898,
  "model_score": 0.4998,
  "style_score": 0.4748,
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
  "content_id": "9aa886fc-84a9-40ca-bdd3-57e167d89ca6",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4841,
  "model_score": 0.6401,
  "style_score": 0.25,
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
  "content_id": "fa4d7185-ca6c-4ab9-aaaa-d6e14d4fe589",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.6164,
  "model_score": 0.5583,
  "style_score": 0.7035,
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
  "content_id": "8f6e2eb5-6c41-4794-b45d-a50ce64e0986",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.3004,
  "model_score": 0.0006,
  "style_score": 0.75,
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
  "content_id": "4388dbdc-1d2a-43ae-b1a2-1b48f0fecbba",
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
  "content_id": "e3a32df2-ff80-46d2-8873-b137c1e35a3a",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.8986,
  "model_score": 0.9976,
  "style_score": 0.75,
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
  "content_id": "d5fead67-3b42-44a0-b10c-e72c7c0572e9",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.8981,
  "model_score": 0.9969,
  "style_score": 0.75,
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
  "content_id": "e6504a4a-17b2-41b7-8039-e29688acd3ab",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.8438,
  "model_score": 0.9064,
  "style_score": 0.75,
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
  "content_id": "963781e6-375d-4456-b815-17c7a058e5b4",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3172,
  "model_score": 0.0287,
  "style_score": 0.75,
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
  "content_id": "61fd7778-be83-4292-acec-39fcb7992453",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3172,
  "model_score": 0.0287,
  "style_score": 0.75,
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
  "content_id": "ef9b3a26-0bf6-48d9-833f-b1d4bbc71e4e",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3172,
  "model_score": 0.0287,
  "style_score": 0.75,
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
  "content_id": "77848998-1e90-45d6-abbb-4b2f0bc710bb",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3172,
  "model_score": 0.0287,
  "style_score": 0.75,
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
  "content_id": "0d729964-160b-4a78-a995-95feeb3e7c45",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3172,
  "model_score": 0.0287,
  "style_score": 0.75,
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
  "content_id": "8166a6d1-6164-49e9-b620-648d70e25e62",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3172,
  "model_score": 0.0287,
  "style_score": 0.75,
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
  "content_id": "a4151932-fd2e-4f90-aa31-dd37f7c0f200",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3172,
  "model_score": 0.0287,
  "style_score": 0.75,
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
  "content_id": "12d38039-14c0-4d6e-9de4-f8ae10501d08",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3172,
  "model_score": 0.0287,
  "style_score": 0.75,
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
  "content_id": "6801dc1d-d625-4a52-ad7b-81b3c9c5ae7e",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3172,
  "model_score": 0.0287,
  "style_score": 0.75,
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
  "content_id": "04700f70-1112-4a3b-8700-d4c7ee9bb287",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3172,
  "model_score": 0.0287,
  "style_score": 0.75,
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
