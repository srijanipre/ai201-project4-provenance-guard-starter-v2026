"""
Turning two numbers into one, and one number into something a person can read.


Two functions live here: the combining rule and the label mapping.

`combine_signals` is where your false-positive decision from Milestone 1
actually gets made. Everything above it — the labels, the appeal path — is
downstream of a number this function produced.

`score_to_label` is where you stop writing for a machine and start writing for
a person. A score of 0.62 means nothing to a writer.

⚠️ Your README's **Signals and Scoring** section has to name the file and
function holding your combining rule. The grader checks your code against what
you claim, so that line should read `scoring.py::combine_signals`.
"""

import config


def combine_signals(model_score: float, style_score: float) -> float:
    """
    Combine two 0–1 signals into one 0–1 AI-likelihood score.

    The rule is a weighted average, with the weights from config.py divided by
    their sum so they don't have to add to 1. Both inputs point the same way,
    higher means more AI-like, and so does the output.

    What happens when the two disagree: with the current weights, a model score
    of 0.9 and a style score of 0.1 combine to 0.58. That's still in the unsure
    band (see score_to_label). A plain average means a strong push from one
    signal can win, so a split isn't automatically unsure. The 0.6 / 0.4 weights
    mean the model gets the bigger say in a split.

    Note the output is a score, not a calibrated probability that a person or a
    model wrote the text.
    """
    for name, value in (("model_score", model_score), ("style_score", style_score)):
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must be between 0 and 1, got {value}")

    total = config.WEIGHT_MODEL_SIGNAL + config.WEIGHT_STYLE_SIGNAL
    combined = (
        config.WEIGHT_MODEL_SIGNAL * model_score
        + config.WEIGHT_STYLE_SIGNAL * style_score
    ) / total
    return round(min(max(combined, 0.0), 1.0), 4)


def score_to_label(score: float) -> tuple[str, str]:
    """
    Turn a combined score into a guess and the text a reader actually sees.

    Returns:
        (guess, label_text) — `guess` is "ai", "human" or "unsure", and
        `label_text` is the sentence shown to the writer.

    The ranges come from config.py and are half-open so every score lands in
    exactly one label:
        score < HUMAN_THRESHOLD              -> human
        HUMAN_THRESHOLD <= score < AI_THRESHOLD -> unsure
        score >= AI_THRESHOLD                -> ai
    """
    if score >= config.AI_THRESHOLD:
        return "ai", (
            "Parts of this writing match patterns often found in machine-generated "
            "text. That's an automated estimate, not proof of how it was written, "
            "and the writer can appeal it for a review."
        )
    if score < config.HUMAN_THRESHOLD:
        return "human", (
            "We think this was probably written by a person. No automated check is "
            "perfect, so this is an estimate rather than a guarantee."
        )
    return "unsure", (
        "We couldn't tell with enough confidence whether a person or an AI wrote "
        "this. Plenty of human writing looks machine-like to automated checks, so "
        "no conclusion is drawn from this result."
    )


def label_ranges() -> list[tuple[str, str]]:
    """
    The score range each label covers. Your README needs these beside the
    label text — given to you so the numbers can't drift apart from config.py.
    """
    return [
        ("high-confidence human", f"below {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f"{config.HUMAN_THRESHOLD:.2f} up to {config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} and above"),
    ]
