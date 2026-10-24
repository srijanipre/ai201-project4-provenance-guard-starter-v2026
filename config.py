"""
Settings for Provenance Guard.

Everything you're likely to change lives here, at the top, on purpose.

You'll edit the thresholds in Milestone 5 and the rate limits in unit 8.
"""

import os
from pathlib import Path

ROOT = Path(__file__).parent


# ─── The service ─────────────────────────────────────────────────────────────

# `127.0.0.1` is loopback — only your own machine can reach it, which is what
# you want all through units 7 and 8. A host somewhere else has to accept
# traffic from outside the box, and that means `0.0.0.0`. Setting the env var
# is how you get it; the default keeps your local `curl` commands unchanged.
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "5000"))

# Flask's debug mode gives anyone who can reach the service an interactive
# Python prompt inside your process. Fine on loopback, a gift to strangers
# anywhere else — so it turns itself off the moment HOST isn't loopback.
DEBUG = os.getenv("AI201_DEBUG", "1") == "1" and HOST in ("127.0.0.1", "localhost")


# ─── The local model ─────────────────────────────────────────────────────────
# Your first signal runs a language model ON YOUR OWN MACHINE. No account, no
# key, no card. It downloads about 550 MB the first time — do that before
# class, not during it.
#
# What it measures: how *predictable* your text is to a language model. Text a
# model finds easy to predict tends to be text a model wrote.
#
# The first call is the slow one — ten to twenty seconds while the model loads,
# longer on an older laptop. After that it stays in memory and a submission
# takes a second or two. That cost is part of what you're learning: this is
# what running a model inline in a request actually looks like.

DETECTOR_MODEL = os.getenv("AI201_DETECTOR_MODEL", "gpt2")

# Longer text gives a steadier reading but takes longer. 400 tokens is roughly
# 300 words, which is enough for the signal to mean something.
DETECTOR_MAX_TOKENS = 400


# ─── Submissions ─────────────────────────────────────────────────────────────
# Longer than this is refused with a 413. About 1,500 words, which is well past
# what a single essay submission needs and keeps the stylometry pass cheap.
# Note the detector only reads the first DETECTOR_MAX_TOKENS of it.

MAX_TEXT_CHARS = 10_000


# ─── Scoring (Milestone 4) ───────────────────────────────────────────────────
# How much each signal counts toward the combined score. The combined score is
# the weighted average of the two signals, divided by the weight total.
#
# Why 0.6 / 0.4: on the calibration set (samples/calibration.json) the model
# signal separated clearly-AI text from human text by roughly 0.20 on average,
# and the style signal by roughly 0.07. The style signal's type-token component
# also ran backwards on that set, so it gets less say. This was decided after
# looking at those numbers, which is worth knowing when you read it.

WEIGHT_MODEL_SIGNAL = 0.6
WEIGHT_STYLE_SIGNAL = 0.4

# Reference points for turning the three style measures into 0–1 components
# (see stylometry.style_signal). These set where "fully human-like" and "fully
# AI-like" sit on each raw measure. They're scale choices, not fitted values.
STYLE_SPREAD_HUMAN_CV = 1.0     # sentence-length CV at or above this reads fully human
STYLE_TTR_AI = 0.5              # moving-average TTR at or below this reads fully AI
STYLE_TTR_HUMAN = 0.9           # moving-average TTR at or above this reads fully human
STYLE_PUNCT_HUMAN_RATE = 0.12   # clause punctuation per word at or above this reads fully human


# ─── Thresholds (Milestone 5) ────────────────────────────────────────────────
# Where one label becomes another. Scores run 0.0 (confidently human) to 1.0
# (confidently AI). Ranges are half-open, so every score lands in exactly one:
#
#   score < HUMAN_THRESHOLD                       -> high-confidence human
#   HUMAN_THRESHOLD <= score < AI_THRESHOLD       -> unsure
#   score >= AI_THRESHOLD                         -> high-confidence AI
#
# The AI threshold is set high on purpose. Formal human writing lands around
# 0.5 on the calibration set, so a 0.70 bar means a human has to look clearly
# machine-like on both signals before the label is "high-confidence AI". The
# cost is that most AI text ends up in the unsure band too.

HUMAN_THRESHOLD = 0.35
AI_THRESHOLD = 0.70


# ─── Rate limiting (UNIT 8) ──────────────────────────────────────────────────
# Off in unit 7. You turn it on and choose the numbers in unit 8, Milestone 1.
#
# Think about two people: a real writer submitting their own work a few times
# an hour, and a script sending a thousand variations to map your thresholds.
# Your README has to say why your numbers and not others.

RATE_LIMITING_ENABLED = os.getenv("AI201_RATE_LIMITS", "0") == "1"

RATE_LIMIT_PER_MINUTE = 10
RATE_LIMIT_PER_DAY = 200

# Flask-Limiter warns loudly without this. In-memory is right for one laptop
# and wrong for anything real — a restart forgets every count, and two copies
# of the service wouldn't share limits.
RATE_LIMIT_STORAGE = "memory://"


# ─── Paths ───────────────────────────────────────────────────────────────────

LOG_DIR = ROOT / "logs"
AUDIT_LOG = LOG_DIR / "audit.jsonl"
RESULTS_DIR = ROOT / "results"
