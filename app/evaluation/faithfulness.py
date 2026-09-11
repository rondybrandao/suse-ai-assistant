# Calcular resposta x contexto (faithfulness)
def calculate_faithfulness(
    answer,
    contexts,
    relevant_keywords,
):
    context_text = " ".join(contexts).lower()
    answer_lower = answer.lower()

    answer_keywords = [
        keyword
        for keyword in relevant_keywords
        if keyword.lower() in answer_lower
    ]

    if not answer_keywords:
        return 0.0

    supported_keywords = [
        keyword
        for keyword in answer_keywords
        if keyword.lower() in context_text
    ]

    return len(supported_keywords) / len(answer_keywords)