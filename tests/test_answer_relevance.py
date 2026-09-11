from app.rag.embeddings import generate_embeddings
from app.rag.qdrant_client import search_similar
from app.rag.generator import generate_answer

from app.evaluation.answer_relevance import (
    calculate_answer_relevance,
)

query = "Como funciona o processo de fechamento de uma OS?"

relevant_keywords = [
    "fechamento",
    "finalização",
    "encerramento",
]

query_embedding = generate_embeddings([query])[0]

results = search_similar(
    query_embedding,
    limit=5,
)

contexts = [
    result.payload["text"]
    for result in results
]

answer = generate_answer(
    query,
    contexts,
)

score = calculate_answer_relevance(
    query,
    answer,
    relevant_keywords
)

print()
print("========================================")
print("AVALIAÇÃO DA RESPOSTA")
print("========================================")

print(f"Pergunta: {query}")

print()
print("Resposta:")
print(answer)

print()
print(f"Answer Relevance: {score:.2f}")


if score >= 0.50:
    print()
    print("ANSWER RELEVANCE: OK")
else:
    print()
    print("ANSWER RELEVANCE: BAIXO")