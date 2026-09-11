# Calcular relevancia
def calculate_answer_relevance(
        question,
        answer,
        relevant_keywords,
):
    question_lower = question.lower()
    answer_lower = answer.lower()

    relevant_question_keywords = [
        keyword,
        for keyword in relevant_keywords
        if keyword.lower() in question_lower
    ]

    if not relevant_question_keywords:
        return 0.0

    matches = sum(
        1
        for keyword in relevant_question_keywords
        if keyword.lower() in answer_lower
    )

    return matches / len(relevant_question_keywords)