"""
Focused tests for Provenance Guard.

    python -m unittest discover -s tests -v

The route tests write to a temporary audit log, so they never touch
logs/audit.jsonl. The few that score real text load gpt2, so the first run is
slow.
"""

import json
import random
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import config  # noqa: E402
import scoring  # noqa: E402
import stylometry  # noqa: E402
import app as appmod  # noqa: E402


class StylometryTests(unittest.TestCase):
    def test_single_sentence_has_no_spread(self):
        self.assertEqual(stylometry.sentence_length_spread("Just one sentence here."), 0.0)

    def test_spread_is_higher_for_uneven_sentences(self):
        flat = "The cat sat down now. The dog ran far off. The bird flew up high."
        uneven = (
            "Yes. The long afternoon stretched on forever while everyone waited "
            "for the bus that never came. Fine."
        )
        self.assertGreater(
            stylometry.sentence_length_spread(uneven),
            stylometry.sentence_length_spread(flat),
        )

    def test_repeated_words_lower_the_ratio(self):
        varied = "Every single word in this sentence is a different word entirely."
        repeated = "the the the the the the the the the the the the"
        self.assertLess(
            stylometry.type_token_ratio(repeated),
            stylometry.type_token_ratio(varied),
        )

    def test_ratio_is_comparable_across_lengths(self):
        rng = random.Random(0)
        vocab = [f"w{i}" for i in range(300)]
        short = " ".join(rng.choice(vocab) for _ in range(200))
        long = " ".join(rng.choice(vocab) for _ in range(2000))
        self.assertAlmostEqual(
            stylometry.type_token_ratio(short),
            stylometry.type_token_ratio(long),
            delta=0.05,
        )

    def test_punctuation_counts_clause_marks_only(self):
        text = "Well, yes; maybe: it's fine (mostly) — well-known. End."
        self.assertGreater(stylometry.punctuation_density(text), 0.0)
        self.assertEqual(stylometry.punctuation_density("Plain words only here."), 0.0)

    def test_empty_inputs_are_safe(self):
        self.assertEqual(stylometry.sentence_length_spread(""), 0.0)
        self.assertEqual(stylometry.type_token_ratio(""), 0.0)
        self.assertEqual(stylometry.punctuation_density(""), 0.0)
        self.assertEqual(stylometry.style_signal("   "), 0.5)

    def test_style_signal_stays_in_range(self):
        samples = [
            "",
            "One.",
            "word " * 500,
            "Café naïve résumé 你好 \U0001F600 ok.",
            "No punctuation at all and it just keeps going and going and going",
        ]
        for text in samples:
            score = stylometry.style_signal(text)
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)

    def test_style_signal_depends_on_text(self):
        plain = (
            "I went home. It was late. I was tired. The dog was asleep. "
            "I ate some soup and went to bed early."
        )
        other = (
            "Although the committee had deliberated for many hours, its members, "
            "weary and divided, ultimately deferred the question; a further review, "
            "they agreed, would be necessary (and perhaps unavoidable)."
        )
        self.assertNotEqual(stylometry.style_signal(plain), stylometry.style_signal(other))


class ScoringTests(unittest.TestCase):
    def test_combine_is_weighted_average(self):
        expected = config.WEIGHT_MODEL_SIGNAL * 1.0
        self.assertAlmostEqual(scoring.combine_signals(1.0, 0.0), round(expected, 4), places=4)
        self.assertAlmostEqual(
            scoring.combine_signals(0.4, 0.8),
            round(0.4 * config.WEIGHT_MODEL_SIGNAL + 0.8 * config.WEIGHT_STYLE_SIGNAL, 4),
            places=4,
        )

    def test_combine_bounds(self):
        self.assertEqual(scoring.combine_signals(0.0, 0.0), 0.0)
        self.assertEqual(scoring.combine_signals(1.0, 1.0), 1.0)

    def test_combine_rejects_out_of_range(self):
        with self.assertRaises(ValueError):
            scoring.combine_signals(1.2, 0.5)
        with self.assertRaises(ValueError):
            scoring.combine_signals(0.5, -0.1)

    def test_disagreement_lands_in_unsure(self):
        combined = scoring.combine_signals(0.95, 0.05)
        self.assertEqual(scoring.score_to_label(combined)[0], "unsure")

    def test_threshold_boundaries(self):
        h, a = config.HUMAN_THRESHOLD, config.AI_THRESHOLD
        cases = [
            (0.0, "human"),
            (round(h - 0.0001, 4), "human"),
            (h, "unsure"),
            (round(a - 0.0001, 4), "unsure"),
            (a, "ai"),
            (1.0, "ai"),
        ]
        for score, want in cases:
            with self.subTest(score=score):
                self.assertEqual(scoring.score_to_label(score)[0], want)

    def test_0_51_and_0_95_differ(self):
        self.assertNotEqual(
            scoring.score_to_label(0.51)[0],
            scoring.score_to_label(0.95)[0],
        )

    def test_every_label_is_reachable(self):
        seen = {scoring.score_to_label(s / 100)[0] for s in range(101)}
        self.assertEqual(seen, {"ai", "human", "unsure"})

    def test_label_text_is_not_a_bare_number(self):
        for score in (0.1, 0.5, 0.9):
            text = scoring.score_to_label(score)[1]
            self.assertIn(" ", text)
            self.assertFalse(any(ch.isdigit() for ch in text))

    def test_label_ranges_match_config(self):
        ranges = dict(scoring.label_ranges())
        self.assertEqual(ranges["high-confidence human"], f"below {config.HUMAN_THRESHOLD:.2f}")
        self.assertEqual(ranges["high-confidence AI"], f"{config.AI_THRESHOLD:.2f} and above")


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.log_path = Path(self.tmp.name) / "audit.jsonl"
        self.patches = [
            mock.patch.object(config, "AUDIT_LOG", self.log_path),
            mock.patch.object(config, "LOG_DIR", Path(self.tmp.name)),
        ]
        for p in self.patches:
            p.start()
        appmod.app.config["TESTING"] = True
        self.client = appmod.app.test_client()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.tmp.cleanup()

    def entries(self):
        if not self.log_path.exists():
            return []
        return [json.loads(line) for line in self.log_path.read_text().splitlines() if line.strip()]

    def submit(self, body):
        return self.client.post("/submit", json=body)

    def test_bad_bodies_return_4xx_and_log_nothing(self):
        bad = [
            None,
            ["text"],
            {"creator_id": "w"},
            {"text": "", "creator_id": "w"},
            {"text": "   ", "creator_id": "w"},
            {"text": None, "creator_id": "w"},
            {"text": 42, "creator_id": "w"},
            {"text": "Hello there friend, how are you?"},
            {"text": "Hello there friend, how are you?", "creator_id": "  "},
            {"text": "word " * 3000, "creator_id": "w"},
        ]
        for body in bad:
            with self.subTest(body=str(body)[:60]):
                if body is None:
                    resp = self.client.post("/submit", data="not json", content_type="application/json")
                else:
                    resp = self.submit(body)
                self.assertGreaterEqual(resp.status_code, 400)
                self.assertLess(resp.status_code, 500)
                self.assertIn("error", resp.get_json())
        self.assertEqual(self.entries(), [])

    def test_submit_with_controlled_scores_hits_each_label(self):
        cases = [(0.9, 0.9, "ai"), (0.1, 0.1, "human"), (0.5, 0.5, "unsure")]
        for model, style, want in cases:
            with self.subTest(want=want):
                with mock.patch.object(appmod.detector, "model_signal", return_value=model), \
                        mock.patch.object(appmod.stylometry, "style_signal", return_value=style):
                    resp = self.submit({"text": "Some ordinary sentence here. Another one.", "creator_id": "w"})
                self.assertEqual(resp.status_code, 200)
                body = resp.get_json()
                self.assertEqual(body["guess"], want)
                self.assertIn("content_id", body)
                self.assertIn("label", body)
                self.assertIn("model_score", body)
                self.assertIn("style_score", body)

    def test_submit_logs_all_scores(self):
        with mock.patch.object(appmod.detector, "model_signal", return_value=0.8), \
                mock.patch.object(appmod.stylometry, "style_signal", return_value=0.6):
            body = self.submit({"text": "Some ordinary sentence here. Another one.", "creator_id": "w"}).get_json()
        entry = self.entries()[-1]
        self.assertEqual(entry["content_id"], body["content_id"])
        self.assertEqual(entry["model_score"], 0.8)
        self.assertEqual(entry["style_score"], 0.6)
        self.assertEqual(entry["combined_score"], body["confidence"])
        self.assertEqual(entry["status"], "decided")

    def test_real_model_submission(self):
        resp = self.submit({
            "text": "I went to the store today. It was raining. I bought milk and bread.",
            "creator_id": "writer123",
        })
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        for key in ("content_id", "guess", "confidence", "label", "model_score", "style_score"):
            self.assertIn(key, body)
        self.assertTrue(0.0 <= body["confidence"] <= 1.0)

    def test_appeal_full_flow(self):
        with mock.patch.object(appmod.detector, "model_signal", return_value=0.9), \
                mock.patch.object(appmod.stylometry, "style_signal", return_value=0.9):
            cid = self.submit({"text": "Some ordinary sentence here. Another one.", "creator_id": "w"}).get_json()["content_id"]

        resp = self.client.post("/appeal", json={"content_id": cid, "reasoning": "I wrote every word."})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["status"], "under_review")

        kinds = [e.get("event", "decision") for e in self.entries() if e.get("content_id") == cid]
        self.assertEqual(kinds, ["decision", "appeal"])

        again = self.client.post("/appeal", json={"content_id": cid, "reasoning": "again"})
        self.assertEqual(again.status_code, 409)

    def test_appeal_unknown_id_is_404_and_logs_nothing(self):
        resp = self.client.post("/appeal", json={"content_id": "nope", "reasoning": "x"})
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(self.entries(), [])

    def test_appeal_bad_bodies(self):
        cases = [
            {"reasoning": "x"},
            {"content_id": "", "reasoning": "x"},
            {"content_id": 5, "reasoning": "x"},
            {"content_id": "abc"},
            {"content_id": "abc", "reasoning": "   "},
        ]
        for body in cases:
            with self.subTest(body=body):
                resp = self.client.post("/appeal", json=body)
                self.assertIn(resp.status_code, (400, 404))
                self.assertIn("error", resp.get_json())

    def test_health_and_ping_still_work(self):
        self.assertEqual(self.client.post("/ping", json={"message": "hi"}).status_code, 200)
        self.assertEqual(self.client.get("/health").status_code, 200)
        self.assertEqual(self.client.get("/log").status_code, 200)


if __name__ == "__main__":
    unittest.main()
