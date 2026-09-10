from app.rag.embeddings import generate_embeddings
from app.rag.qdrant_client import search_similar

from app.evaluation.context_relevance import (
    calculate_context_relevance,
)

query = "Como funciona o processo de fechamento de uma OS?"

relevant_keywords = [
    "finalização",
    "finalizado",
    "encerramento",
    "histórico",
    "financeiro",
]

query_embedding = generate_embeddings([query])[0]

results = search_similar(
    query_embedding,
    limit=5
)

retrieved_contexts = [
    result.payload["text"]
    for result in results 
]

score = calculate_context_relevance(
    retrieved_contexts,
    relevant_keywords
)

print(f"Pergunta: {query}")
print(f"Contextos avaliados: {len(retrieved_contexts)}")
print(f"Context Relevance: {score:.2f}")

if score >= 0.50:
    print()
    print("Context Relevance: OK")
else:
    print()
    print("Context Relevance: Baixo")