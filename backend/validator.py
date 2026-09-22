def validate_answer(question, answer):

    if not answer:
        return False

    question_lower = question.lower().strip()
    answer_lower = answer.lower().strip().rstrip(".")

    # The generator explicitly abstained.
    if "not enough information" in answer_lower:
        return False

    descriptive_starters = (
        "what ",
        "why ",
        "how "
    )

    # A bare Yes/No does not answer a descriptive question.
    if question_lower.startswith(descriptive_starters):
        if answer_lower in ("yes", "no"):
            return False

    return True