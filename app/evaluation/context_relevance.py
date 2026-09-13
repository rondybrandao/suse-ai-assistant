import numpy as np

from app.rag.embeddings import generate_embeddings

# calcular a relevancia docontexto (simples)
def calculate_context_relevance_simple(
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


def cosine_similarity(vector_a, vector_b):
    """
    Calcula a similaridade de cosseno entre dois vetores.

    Resultado:
    1.0  -> textos semanticamente muito próximos
    0.0  -> pouca relação semântica
    """

    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return np.dot(vector_a, vector_b) / (norm_a * norm_b)



def calculate_context_relevance(
        question,
        retrieved_contexts,
):
    """
    Mede a relevância semântica dos contextos recuperados
    em relação à pergunta.

    Quanto maior o valor, maior a similaridade semântica.
    """

    if not retrieved_contexts:
        return 0.0

    # Gera embedding da pergunta.
    question_embedding = generate_embeddings(
        [question]
    )[0]

    # Gera embeddings dos contextos recuperados.
    context_embeddings = generate_embeddings(
        retrieved_contexts
    )

    scores = []

    for context_embedding in context_embeddings:
        score = cosine_similarity(
            question_embedding,
            context_embedding,
        )

        scores.append(score)

    # Media da similaridade dos contextos
    return float(np.mean(scores))