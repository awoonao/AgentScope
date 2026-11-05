import re


def normalize_answer(text):
    """Normalize whitespace and capitalization."""
    return re.sub(r"\s+", " ", str(text).strip().lower())


def evaluate_answer(actual, expected):
    """
    Conservative evaluator for simple numerical
    and short factual answers.

    Returns:
        correct
        incorrect
        needs_review
    """
    actual = normalize_answer(actual)
    expected = normalize_answer(expected)

    if not actual or not expected:
        return "needs_review"

    # Exact match
    if actual.strip(" .!") == expected:
        return "correct"

    # Match expected value as a standalone token
    pattern = r"(?<!\w)" + re.escape(expected) + r"(?!\w)"
    matches = list(re.finditer(pattern, actual))

    if not matches:
        return "incorrect"

    # Flag common negation patterns.
    negation_patterns = [
        rf"\bnot\s+{re.escape(expected)}\b",
        rf"\bnever\s+{re.escape(expected)}\b",
        rf"\bisn't\s+{re.escape(expected)}\b",
        rf"\bnot\b.*\b{re.escape(expected)}\b",

        # Negation appearing after the expected answer
        rf"\b{re.escape(expected)}\b.*\bnot\b",
        rf"\b{re.escape(expected)}\b.*\bnever\b",
        rf"\b{re.escape(expected)}\b.*\bisn't\b",
    ]

    for negation in negation_patterns:
        if re.search(negation, actual):
            return "needs_review"

    # Flag potentially conflicting or uncertain answers.
    uncertainty_patterns = [
        r"\bcould be\b",
        r"\bmight be\b",
        r"\bmaybe\b",
        r"\bperhaps\b",
        r"\bor\b"
    ]

    if any(re.search(p, actual) for p in uncertainty_patterns):
        return "needs_review"

    # If the expected answer appears within a
    # longer explanation, flag for review rather
    # than automatically accepting it.
    if len(actual.split()) > 8:
        return "needs_review"

    return "correct"


if __name__ == "__main__":
    examples = [
        ("5 + 5 = 10", "10"),
        ("The answer is not 10.", "10"),
        ("The answer is 100.", "10"),
        ("The answer could be 10 or 11.", "10"),
        ("Paris is not the capital of France.", "Paris"),
    ]

    for actual, expected in examples:
        print(actual, "->", evaluate_answer(actual, expected))
