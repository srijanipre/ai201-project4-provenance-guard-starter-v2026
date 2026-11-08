# Run log — unit9_harness-check_t1

- Produced by: `run_eval.py::main`
- Service: `app.py::submit` · scoring: `scoring.py::combine_signals`
- 1 trials per criterion · 2026-11-08 14:39

Each Run cell is the number the criterion names, measured by the
scenario's check in `scenarios.py`. MET means all three trials held.

| Criterion | Target | Run 1 | Verdict |
|---|---|---|---|
| 1. human passages | ≤ 1 of 10 labelled AI, every run | 0/10 AI (held) | MET |
| 2. AI vs human separation | mean AI − mean human ≥ 0.30 | gap 0.201 (missed) | MISSED |
| 3. label coverage | all 3 labels from real text; 6/6 boundary checks | 3/3 labels, 6/6 bounds (held) | MET |
| 4. appeal path | 5/5 appeals; 3/3 error cases | 5/5 appeals, 3/3 errors (held) | MET |
| 5. malformed input | 8/8 4xx with `error`, 0 decisions logged | 8/8 clean, 0 decisions logged (held) | MET |

---

## What actually came back

Real output. Paste the relevant parts into your README — the rubric
asks for the actual JSON, not a description of it.

### human passages

**Trial 1**

```json
[
  {
    "status": 200,
    "content_id": "15055184-6a86-4ba1-9deb-1e7fcd26409e",
    "guess": "human",
    "confidence": 0.2985,
    "model_score": 0.4097,
    "style_score": 0.1316,
    "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
    "has_error_key": false,
    "sent": "You don\u2019t know about me without you have read a book by the name of Th"
  },
  {
    "status": 200,
    "content_id": "19b86a91-e5d9-42a6-b41d-02fd00699b52",
    "guess": "unsure",
    "confidence": 0.4773,
    "model_score": 0.4691,
    "style_score": 0.4896,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "After supper she got out her book and learned me about Moses and the B"
  },
  {
    "status": 200,
    "content_id": "7ead369d-bc10-4b70-8db9-b27f2cc855ca",
    "guess": "unsure",
    "confidence": 0.4223,
    "model_score": 0.5117,
    "style_score": 0.2881,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "Pretty soon I wanted to smoke, and asked the widow to let me. But she "
  },
  {
    "status": 200,
    "content_id": "364e25f3-acfb-41bb-be46-6ccde81991c6",
    "guess": "human",
    "confidence": 0.2653,
    "model_score": 0.2541,
    "style_score": 0.2822,
    "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
    "has_error_key": false,
    "sent": "And now it was that, being on some occasion made ashamed of my ignoran"
  },
  {
    "status": 200,
    "content_id": "46a870b5-fd50-4ba6-b96d-7c2f5ad57a4e",
    "guess": "unsure",
    "confidence": 0.4394,
    "model_score": 0.5656,
    "style_score": 0.25,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "In the evening I found myself very feverish, and went in to bed; but, "
  },
  {
    "status": 200,
    "content_id": "92e664bc-6ad3-478e-8452-167cb4859ba2",
    "guess": "unsure",
    "confidence": 0.5772,
    "model_score": 0.622,
    "style_score": 0.5101,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "The subject of this Essay is not the so-called Liberty of the Will, so"
  },
  {
    "status": 200,
    "content_id": "939a1e13-6e5c-46fe-9b4c-3b7b3868b717",
    "guess": "unsure",
    "confidence": 0.618,
    "model_score": 0.7481,
    "style_score": 0.4228,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "No society in which these liberties are not, on the whole, respected, "
  },
  {
    "status": 200,
    "content_id": "6a80a21a-236d-4689-9492-db452c571415",
    "guess": "unsure",
    "confidence": 0.5768,
    "model_score": 0.5984,
    "style_score": 0.5444,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "First: the opinion which it is attempted to suppress by authority may "
  },
  {
    "status": 200,
    "content_id": "142e8ccb-243d-450b-b529-4cf95a3b1d5b",
    "guess": "unsure",
    "confidence": 0.5666,
    "model_score": 0.598,
    "style_score": 0.5194,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "Strange it is, that men should admit the validity of the arguments for"
  },
  {
    "status": 200,
    "content_id": "cf704d33-458d-4089-869f-9576a37b2b45",
    "guess": "unsure",
    "confidence": 0.3908,
    "model_score": 0.3805,
    "style_score": 0.4063,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "Most men, even in this comparatively free country, through mere ignora"
  }
]
```

Check (`scenarios.py::check_false_positives`):

```json
{
  "value": "0/10 AI",
  "passed": true,
  "false_positives": 0,
  "guesses": [
    "human",
    "unsure",
    "unsure",
    "human",
    "unsure",
    "unsure",
    "unsure",
    "unsure",
    "unsure",
    "unsure"
  ]
}
```

### AI vs human separation

**Trial 1**

```json
[
  {
    "status": 200,
    "content_id": "513292f8-d6b8-48fc-96d4-2a041492e944",
    "guess": "unsure",
    "confidence": 0.576,
    "model_score": 0.5525,
    "style_score": 0.6113,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "Remote work has changed how many teams operate, and the effects are bo"
  },
  {
    "status": 200,
    "content_id": "2e824bc6-c883-4e3d-ab92-584ad8556ea4",
    "guess": "ai",
    "confidence": 0.7836,
    "model_score": 0.8938,
    "style_score": 0.6184,
    "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.",
    "has_error_key": false,
    "sent": "Photosynthesis is the process by which plants, algae, and some bacteri"
  },
  {
    "status": 200,
    "content_id": "211b108d-307b-4767-a609-af57a0d9544d",
    "guess": "ai",
    "confidence": 0.7322,
    "model_score": 0.7947,
    "style_score": 0.6384,
    "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.",
    "has_error_key": false,
    "sent": "When designing a budget, individuals should begin by clearly identifyi"
  },
  {
    "status": 200,
    "content_id": "b06ce1e6-d3c8-409c-9136-00b0ab6de16f",
    "guess": "unsure",
    "confidence": 0.5342,
    "model_score": 0.5957,
    "style_score": 0.4419,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "Effective customer feedback is a valuable resource for any product tea"
  },
  {
    "status": 200,
    "content_id": "5bfb9929-f468-4de8-bb26-f597fe94120d",
    "guess": "unsure",
    "confidence": 0.693,
    "model_score": 0.7356,
    "style_score": 0.629,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "The history of the printing press is a story of gradual transformation"
  },
  {
    "status": 200,
    "content_id": "6d5fd355-0419-417c-a076-fcda73ba409d",
    "guess": "human",
    "confidence": 0.2985,
    "model_score": 0.4097,
    "style_score": 0.1316,
    "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
    "has_error_key": false,
    "sent": "You don\u2019t know about me without you have read a book by the name of Th"
  },
  {
    "status": 200,
    "content_id": "e36523d2-1330-4a20-b942-4349dac984cd",
    "guess": "unsure",
    "confidence": 0.4773,
    "model_score": 0.4691,
    "style_score": 0.4896,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "After supper she got out her book and learned me about Moses and the B"
  },
  {
    "status": 200,
    "content_id": "a8b300a2-13f1-462e-a577-6681ff023a92",
    "guess": "unsure",
    "confidence": 0.4223,
    "model_score": 0.5117,
    "style_score": 0.2881,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "Pretty soon I wanted to smoke, and asked the widow to let me. But she "
  },
  {
    "status": 200,
    "content_id": "14393c26-12ec-4360-8909-534813fe5dc8",
    "guess": "human",
    "confidence": 0.2653,
    "model_score": 0.2541,
    "style_score": 0.2822,
    "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
    "has_error_key": false,
    "sent": "And now it was that, being on some occasion made ashamed of my ignoran"
  },
  {
    "status": 200,
    "content_id": "c900c5ab-8ce8-48c4-86cd-06557d14648f",
    "guess": "unsure",
    "confidence": 0.4394,
    "model_score": 0.5656,
    "style_score": 0.25,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "In the evening I found myself very feverish, and went in to bed; but, "
  },
  {
    "status": 200,
    "content_id": "7b9b6977-765f-4f67-8d6f-466de8fe8a64",
    "guess": "unsure",
    "confidence": 0.5772,
    "model_score": 0.622,
    "style_score": 0.5101,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "The subject of this Essay is not the so-called Liberty of the Will, so"
  },
  {
    "status": 200,
    "content_id": "5989cf18-5ed6-4b12-be47-8203c282c451",
    "guess": "unsure",
    "confidence": 0.618,
    "model_score": 0.7481,
    "style_score": 0.4228,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "No society in which these liberties are not, on the whole, respected, "
  },
  {
    "status": 200,
    "content_id": "cfe9bc80-ff61-486d-8383-464c5875a679",
    "guess": "unsure",
    "confidence": 0.5768,
    "model_score": 0.5984,
    "style_score": 0.5444,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "First: the opinion which it is attempted to suppress by authority may "
  },
  {
    "status": 200,
    "content_id": "565246f0-69bf-4c78-b9d8-4905c1baa33f",
    "guess": "unsure",
    "confidence": 0.5666,
    "model_score": 0.598,
    "style_score": 0.5194,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "Strange it is, that men should admit the validity of the arguments for"
  },
  {
    "status": 200,
    "content_id": "d7d80bed-9da6-4db6-83ac-b173aeed6f04",
    "guess": "unsure",
    "confidence": 0.3908,
    "model_score": 0.3805,
    "style_score": 0.4063,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "Most men, even in this comparatively free country, through mere ignora"
  }
]
```

Check (`scenarios.py::check_separation`):

```json
{
  "value": "gap 0.201",
  "passed": false,
  "mean_ai": 0.6638,
  "mean_human": 0.4632,
  "gap": 0.2006
}
```

### label coverage

**Trial 1**

```json
[
  {
    "status": 200,
    "content_id": "461f4153-d2b7-414c-8566-bc519ddb0ccd",
    "guess": "human",
    "confidence": 0.2985,
    "model_score": 0.4097,
    "style_score": 0.1316,
    "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
    "has_error_key": false,
    "sent": "You don\u2019t know about me without you have read a book by the name of Th"
  },
  {
    "status": 200,
    "content_id": "f4af5b2c-94d3-4232-8e26-4f2a759ce339",
    "guess": "unsure",
    "confidence": 0.4773,
    "model_score": 0.4691,
    "style_score": 0.4896,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "After supper she got out her book and learned me about Moses and the B"
  },
  {
    "status": 200,
    "content_id": "826b1a46-cf70-4848-83cc-15077c0b6406",
    "guess": "unsure",
    "confidence": 0.4223,
    "model_score": 0.5117,
    "style_score": 0.2881,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "Pretty soon I wanted to smoke, and asked the widow to let me. But she "
  },
  {
    "status": 200,
    "content_id": "7981a6c3-d33f-4567-8c44-fef50ceb4ea5",
    "guess": "human",
    "confidence": 0.2653,
    "model_score": 0.2541,
    "style_score": 0.2822,
    "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
    "has_error_key": false,
    "sent": "And now it was that, being on some occasion made ashamed of my ignoran"
  },
  {
    "status": 200,
    "content_id": "dcb8d98e-7b9b-4051-a23b-c279a0dd4c1c",
    "guess": "unsure",
    "confidence": 0.4394,
    "model_score": 0.5656,
    "style_score": 0.25,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "In the evening I found myself very feverish, and went in to bed; but, "
  },
  {
    "status": 200,
    "content_id": "12d26944-6e5b-466b-8be1-284d97a6fd71",
    "guess": "unsure",
    "confidence": 0.5772,
    "model_score": 0.622,
    "style_score": 0.5101,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "The subject of this Essay is not the so-called Liberty of the Will, so"
  },
  {
    "status": 200,
    "content_id": "5654472b-f187-43c9-a0f3-34c6818d2ae9",
    "guess": "unsure",
    "confidence": 0.618,
    "model_score": 0.7481,
    "style_score": 0.4228,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "No society in which these liberties are not, on the whole, respected, "
  },
  {
    "status": 200,
    "content_id": "929c952b-80de-457b-bd97-e87f540dcd85",
    "guess": "unsure",
    "confidence": 0.5768,
    "model_score": 0.5984,
    "style_score": 0.5444,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "First: the opinion which it is attempted to suppress by authority may "
  },
  {
    "status": 200,
    "content_id": "d30f06fb-eab3-4ed3-8e04-19c1d36d3647",
    "guess": "unsure",
    "confidence": 0.5666,
    "model_score": 0.598,
    "style_score": 0.5194,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "Strange it is, that men should admit the validity of the arguments for"
  },
  {
    "status": 200,
    "content_id": "f9cf7af2-07d5-40e6-ae28-a369b996f440",
    "guess": "unsure",
    "confidence": 0.3908,
    "model_score": 0.3805,
    "style_score": 0.4063,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "Most men, even in this comparatively free country, through mere ignora"
  },
  {
    "status": 200,
    "content_id": "621df85e-e1d0-46f1-ba1c-d99a7ddcaeb1",
    "guess": "human",
    "confidence": 0.3179,
    "model_score": 0.2873,
    "style_score": 0.3639,
    "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
    "has_error_key": false,
    "sent": "But men labor under a mistake. The better part of the man is soon plow"
  },
  {
    "status": 200,
    "content_id": "d12814be-2c98-4492-98dd-96580e21f175",
    "guess": "unsure",
    "confidence": 0.576,
    "model_score": 0.5525,
    "style_score": 0.6113,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "Remote work has changed how many teams operate, and the effects are bo"
  },
  {
    "status": 200,
    "content_id": "e854476f-f2b9-4216-8a76-a2ee502df97b",
    "guess": "ai",
    "confidence": 0.7836,
    "model_score": 0.8938,
    "style_score": 0.6184,
    "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.",
    "has_error_key": false,
    "sent": "Photosynthesis is the process by which plants, algae, and some bacteri"
  },
  {
    "status": 200,
    "content_id": "c615436c-5ae9-4042-b582-9e33f7f660c7",
    "guess": "ai",
    "confidence": 0.7322,
    "model_score": 0.7947,
    "style_score": 0.6384,
    "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.",
    "has_error_key": false,
    "sent": "When designing a budget, individuals should begin by clearly identifyi"
  },
  {
    "status": 200,
    "content_id": "3c19125d-f7a0-4c60-93cb-2547e99767d4",
    "guess": "unsure",
    "confidence": 0.5342,
    "model_score": 0.5957,
    "style_score": 0.4419,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "Effective customer feedback is a valuable resource for any product tea"
  },
  {
    "status": 200,
    "content_id": "397ef51a-27d4-4e67-9312-3e06190edd55",
    "guess": "unsure",
    "confidence": 0.693,
    "model_score": 0.7356,
    "style_score": 0.629,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "The history of the printing press is a story of gradual transformation"
  },
  {
    "status": 200,
    "content_id": "04a575f3-75dc-4969-ab2f-ef9237588c9c",
    "guess": "unsure",
    "confidence": 0.583,
    "model_score": 0.5879,
    "style_score": 0.5756,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "Remote work has changed how a lot of teams operate, and honestly the e"
  },
  {
    "status": 200,
    "content_id": "94d07435-db99-48e0-ab71-81ef64a99e56",
    "guess": "unsure",
    "confidence": 0.6744,
    "model_score": 0.6586,
    "style_score": 0.6981,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "When you make a budget, start by writing down what you earn and what y"
  },
  {
    "status": 200,
    "content_id": "9eea9f17-b827-4ebb-b969-83c375e1d356",
    "guess": "unsure",
    "confidence": 0.6716,
    "model_score": 0.6046,
    "style_score": 0.7721,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "The history of the printing press is more a story of slow change than "
  }
]
```

Check (`scenarios.py::check_label_coverage`):

```json
{
  "value": "3/3 labels, 6/6 bounds",
  "passed": true,
  "labels_seen": {
    "human": 3,
    "unsure": 14,
    "ai": 2
  },
  "boundaries": [
    {
      "score": 0.0,
      "want": "human",
      "got": "human"
    },
    {
      "score": 0.3499,
      "want": "human",
      "got": "human"
    },
    {
      "score": 0.35,
      "want": "unsure",
      "got": "unsure"
    },
    {
      "score": 0.6999,
      "want": "unsure",
      "got": "unsure"
    },
    {
      "score": 0.7,
      "want": "ai",
      "got": "ai"
    },
    {
      "score": 1.0,
      "want": "ai",
      "got": "ai"
    }
  ]
}
```

### appeal path

**Trial 1**

```json
[
  {
    "status": 200,
    "content_id": "69f8bc13-da33-461f-8429-dcbe8af23114",
    "guess": "ai",
    "confidence": 0.7836,
    "model_score": 0.8938,
    "style_score": 0.6184,
    "label": "Parts of this writing match patterns often found in machine-generated text. That's an automated estimate, not proof of how it was written, and the writer can appeal it for a review.",
    "has_error_key": false,
    "sent": "Photosynthesis is the process by which plants, algae, and some bacteri"
  },
  {
    "status": 200,
    "content_id": "01659eb2-e2f6-4a76-80e2-9e701f5b94a8",
    "guess": "human",
    "confidence": 0.2985,
    "model_score": 0.4097,
    "style_score": 0.1316,
    "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
    "has_error_key": false,
    "sent": "You don\u2019t know about me without you have read a book by the name of Th"
  },
  {
    "status": 200,
    "content_id": "97480228-33a3-4969-8a1f-84bad1417cf7",
    "guess": "unsure",
    "confidence": 0.576,
    "model_score": 0.5525,
    "style_score": 0.6113,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "Remote work has changed how many teams operate, and the effects are bo"
  },
  {
    "status": 200,
    "content_id": "ac6b5365-db6c-4389-8cd3-f9a9fb91d401",
    "guess": "human",
    "confidence": 0.2653,
    "model_score": 0.2541,
    "style_score": 0.2822,
    "label": "We think this was probably written by a person. No automated check is perfect, so this is an estimate rather than a guarantee.",
    "has_error_key": false,
    "sent": "And now it was that, being on some occasion made ashamed of my ignoran"
  },
  {
    "status": 200,
    "content_id": "76bc82e9-ecbe-4fa6-a0b6-b6a744d2f978",
    "guess": "unsure",
    "confidence": 0.618,
    "model_score": 0.7481,
    "style_score": 0.4228,
    "label": "We couldn't tell with enough confidence whether a person or an AI wrote this. Plenty of human writing looks machine-like to automated checks, so no conclusion is drawn from this result.",
    "has_error_key": false,
    "sent": "No society in which these liberties are not, on the whole, respected, "
  }
]
```

Check (`scenarios.py::check_appeals`):

```json
{
  "value": "5/5 appeals, 3/3 errors",
  "passed": true,
  "labels_appealed": [
    "ai",
    "human",
    "unsure"
  ],
  "appeals": [
    {
      "content_id": "69f8bc13-da33-461f-8429-dcbe8af23114",
      "guess": "ai",
      "http": 200,
      "status": "under_review",
      "lines_added": 1,
      "appeal_entry": true,
      "original_intact": true
    },
    {
      "content_id": "01659eb2-e2f6-4a76-80e2-9e701f5b94a8",
      "guess": "human",
      "http": 200,
      "status": "under_review",
      "lines_added": 1,
      "appeal_entry": true,
      "original_intact": true
    },
    {
      "content_id": "97480228-33a3-4969-8a1f-84bad1417cf7",
      "guess": "unsure",
      "http": 200,
      "status": "under_review",
      "lines_added": 1,
      "appeal_entry": true,
      "original_intact": true
    },
    {
      "content_id": "ac6b5365-db6c-4389-8cd3-f9a9fb91d401",
      "guess": "human",
      "http": 200,
      "status": "under_review",
      "lines_added": 1,
      "appeal_entry": true,
      "original_intact": true
    },
    {
      "content_id": "76bc82e9-ecbe-4fa6-a0b6-b6a744d2f978",
      "guess": "unsure",
      "http": 200,
      "status": "under_review",
      "lines_added": 1,
      "appeal_entry": true,
      "original_intact": true
    }
  ],
  "error_cases": [
    {
      "case": "unknown content_id",
      "http": 404,
      "lines_added": 0,
      "ok": true
    },
    {
      "case": "second appeal",
      "http": 409,
      "ok": true
    },
    {
      "case": "malformed body (no reasoning)",
      "http": 400,
      "ok": true
    }
  ]
}
```

### malformed input

**Trial 1**

```json
[
  {
    "status": 400,
    "content_id": null,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "has_error_key": true,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "content_id": null,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "has_error_key": true,
    "sent": "   \n\t "
  },
  {
    "status": 400,
    "content_id": null,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "has_error_key": true,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "content_id": null,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "has_error_key": true,
    "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}"
  },
  {
    "status": 400,
    "content_id": null,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "has_error_key": true,
    "sent": "{\"text\": 12345, \"creator_id\": \"eval_bad_number\"}"
  },
  {
    "status": 400,
    "content_id": null,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "has_error_key": true,
    "sent": "{\"text\": \"A perfectly ordinary sentence with no creator attached to it.\"}"
  },
  {
    "status": 413,
    "content_id": null,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "has_error_key": true,
    "sent": "word word word word word word word word word word word word word word "
  },
  {
    "status": 400,
    "content_id": null,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "has_error_key": true,
    "sent": "(raw, not JSON) this is not json {"
  }
]
```

Check (`scenarios.py::check_malformed`):

```json
{
  "value": "8/8 clean, 0 decisions logged",
  "passed": true,
  "statuses": [
    400,
    400,
    400,
    400,
    400,
    400,
    413,
    400
  ],
  "decision_entries_added": 0,
  "rejected_entries_added": 8
}
```
