"""
tests for the unit 9 request log (requestlog.py)

    python -m unittest discover -s tests -v

both logs go to a temp folder so logs/ doesnt get touched, and the model is
mocked so gpt2 never loads here
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import config  # noqa: E402
import app as appmod  # noqa: E402

FIELDS = ("timestamp", "method", "path", "status", "duration_ms", "in_bytes",
          "in_text_chars", "creator_id", "out_bytes", "content_id", "guess",
          "confidence", "error", "exception", "model_loaded")

TEXT = "Some ordinary sentence here. Another one follows it."


class RequestLogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        tmp = Path(self.tmp.name)
        self.req_log = tmp / "requests.jsonl"
        self.patches = [
            mock.patch.object(config, "AUDIT_LOG", tmp / "audit.jsonl"),
            mock.patch.object(config, "LOG_DIR", tmp),
            mock.patch.object(config, "REQUEST_LOG", self.req_log),
            mock.patch.object(appmod.detector, "model_signal", return_value=0.5),
        ]
        for p in self.patches:
            p.start()
        appmod.app.config["TESTING"] = True
        appmod.limiter.enabled = False
        self.client = appmod.app.test_client()

    def tearDown(self):
        appmod.limiter.enabled = True
        appmod.app.config["PROPAGATE_EXCEPTIONS"] = None
        for p in self.patches:
            p.stop()
        self.tmp.cleanup()

    def lines(self):
        if not self.req_log.exists():
            return []
        return [json.loads(x) for x in self.req_log.read_text().splitlines() if x.strip()]

    def test_one_line_per_request_with_every_field(self):
        self.client.post("/ping", json={"message": "hi"})
        self.client.get("/health")
        self.client.post("/submit", json={"text": TEXT, "creator_id": "w"})
        self.client.get("/log?limit=1")
        lines = self.lines()
        self.assertEqual([e["path"] for e in lines], ["/ping", "/health", "/submit", "/log"])
        for e in lines:
            self.assertEqual(set(e), set(FIELDS))
            self.assertIsInstance(e["duration_ms"], float)

    def test_success_records_output_but_not_the_text(self):
        body = self.client.post("/submit", json={"text": TEXT, "creator_id": "w"}).get_json()
        entry = self.lines()[-1]
        self.assertEqual(entry["status"], 200)
        self.assertEqual(entry["content_id"], body["content_id"])
        self.assertEqual(entry["guess"], body["guess"])
        self.assertEqual(entry["in_text_chars"], len(TEXT))
        self.assertIsNone(entry["error"])
        self.assertNotIn("ordinary sentence", self.req_log.read_text())

    def test_rejection_records_status_and_error_code(self):
        self.client.post("/submit", json={"text": "", "creator_id": "w"})
        self.client.post("/submit", data="not json", content_type="application/json")
        self.client.get("/no-such-route")
        got = [(e["status"], e["error"]) for e in self.lines()]
        self.assertEqual(got, [(400, "empty_text"), (400, "invalid_body"), (404, "http_404")])

    def test_rate_limited_request_is_logged(self):
        appmod.limiter.enabled = True
        appmod.limiter.reset()
        for _ in range(config.RATE_LIMIT_PER_MINUTE + 1):
            self.client.post("/submit", json={"text": TEXT, "creator_id": "flooder"})
        appmod.limiter.reset()
        last = self.lines()[-1]
        self.assertEqual((last["status"], last["error"]), (429, "rate_limited"))
        self.assertIsNotNone(last["duration_ms"])

    def test_unhandled_exception_is_json_500_and_names_the_exception(self):
        appmod.app.config["PROPAGATE_EXCEPTIONS"] = False
        with mock.patch.object(appmod.stylometry, "style_signal", side_effect=RuntimeError("boom")), \
                mock.patch.object(appmod.app.logger, "error"):
            resp = self.client.post("/submit", json={"text": TEXT, "creator_id": "w"})
        self.assertEqual(resp.status_code, 500)
        self.assertEqual(resp.get_json()["error"], "internal_error")
        entry = self.lines()[-1]
        self.assertEqual(entry["status"], 500)
        self.assertEqual(entry["exception"], "RuntimeError: boom")

    def test_audit_log_schema_is_unchanged(self):
        self.client.post("/submit", json={"text": TEXT, "creator_id": "w"})
        entry = json.loads(config.AUDIT_LOG.read_text().splitlines()[-1])
        self.assertEqual(set(entry), {"timestamp", "content_id", "creator_id", "guess",
                                      "model_score", "style_score", "combined_score",
                                      "label", "status"})

    def test_a_broken_request_log_never_breaks_the_response(self):
        with mock.patch("requestlog.write", side_effect=OSError("disk full")), \
                mock.patch("sys.stderr"):
            resp = self.client.post("/ping", json={"message": "hi"})
        self.assertEqual(resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()
