# calcular a relevancia docontexto
def calculate_context_relevance(
        retrieved_contexts,
        relevant_keywords,
):
    if not retrieved_contexts:
        return 0.0

    total_score = 0.0

    for context in retrieved_contexts:
        context_lower = context.lower()

        matches = sum(
            1
            for keyword in relevant_keywords
            if keyword.lower() in context_lower
        )

        score = matches / len(relevant_keywords)

        total_score += score

    return total_score / len(retrieved_contexts)