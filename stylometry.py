"""
Signal two: the style signal.

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

The three measures are below, and style_signal combines them into one score.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Run it from a terminal to see each measure on one piece of text:

    python stylometry.py "some text to look at"
"""

import re
import statistics

import config


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures ───────────────────────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies, as a coefficient of variation.

    Returns the stdev of sentence lengths in words divided by the mean. Higher
    means more uneven, which reads as more human. A text with fewer than two
    sentences has no spread to measure, so it returns 0.0 and `style_signal`
    treats it as "no evidence" instead of as machine-flat.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    if mean == 0:
        return 0.0
    return statistics.stdev(lengths) / mean


def type_token_ratio(text: str) -> float:
    """
    Moving-average type-token ratio, between 0 and 1. Higher means more varied.

    A plain unique/total ratio falls as the text gets longer, so it can't be
    compared across submissions of different lengths. Here it's computed over
    50-word windows and averaged. Texts shorter than one window fall back to the
    plain ratio.
    """
    w = words(text)
    if not w:
        return 0.0
    window = 50
    if len(w) <= window:
        return len(set(w)) / len(w)
    ratios = [
        len(set(w[i:i + window])) / window
        for i in range(len(w) - window + 1)
    ]
    return sum(ratios) / len(ratios)


def punctuation_density(text: str) -> float:
    """
    Clause-level punctuation per word: commas, semicolons, colons, brackets and
    dashes. Full stops and question marks are left out, since every sentence
    has one. Hyphens inside words are left out too.

    Returns a raw rate, usually somewhere around 0.05 to 0.2 per word, so
    `style_signal` has to scale it before it can be mixed with the others.
    """
    marks = re.findall(r"[,;:()\u2014\u2013]", text)
    n = len(words(text))
    if n == 0:
        return 0.0
    return len(marks) / n


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    Each measure is turned into a 0–1 "AI-ish" component, then the three are
    averaged with equal weight.

      - sentence spread: CV of 1.0 or more counts as fully human-like. Flat
        sentences (CV near 0) count as AI-ish. Under three sentences gives no
        real reading, so the component is neutral (0.5).
      - type-token ratio: a moving-average TTR of 0.9 or more counts as fully
        human-like, and 0.5 or less as fully AI-ish, with a straight line in
        between.
      - punctuation: a rate of 0.12 marks per word or more counts as fully
        human-like, and none at all as fully AI-ish.

    The reference points are scale choices written in config.py, not fitted
    numbers.
    """
    if not text.strip():
        return 0.5

    cv = sentence_length_spread(text)
    if len(sentences(text)) < 3:
        spread_ai = 0.5
    else:
        spread_ai = 1.0 - min(cv / config.STYLE_SPREAD_HUMAN_CV, 1.0)

    ttr = type_token_ratio(text)
    lo, hi = config.STYLE_TTR_AI, config.STYLE_TTR_HUMAN
    variety_ai = 1.0 - min(max((ttr - lo) / (hi - lo), 0.0), 1.0)

    punct = punctuation_density(text)
    punct_ai = 1.0 - min(punct / config.STYLE_PUNCT_HUMAN_RATE, 1.0)

    score = (spread_ai + variety_ai + punct_ai) / 3.0
    return round(min(max(score, 0.0), 1.0), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
