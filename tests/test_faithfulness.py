from app.rag.embeddings import generate_embeddings
from app.rag.qdrant_client import search_similar
from app.rag.generator import generate_answer

from app.evaluation.faithfulness import (
    calculate_faithfulness,
)

query = "Como funciona o processo de fechamento de uma OS?"

relevant_keywords = [
    "finalizado",
    "finalização",
    "encerramento",
    "fechamento",
    "histórico",
    "financeiro",
    "metas",
    "CRM",
]

query_embedding = generate_embeddings([query])[0]

results = search_similar(
    query_embedding,
    limit=5
)

contexts = [
    result.payload["text"]
    for result in results
]

answer = generate_answer(
    query,
    contexts,
)

score = calculate_faithfulness(
    answer,
    contexts,
    relevant_keywords
)

print()
print("========================================")
print("AVALIAÇÃO DE FAITHFULNESS")
print("========================================")

print(f"Pergunta: {query}")

print()
print("Resposta:")
print(answer)

print()
print(f"Faithfulness: {score:.2f}")


if score >= 0.50:
    print()
    print("FAITHFULNESS: OK")
    print("A resposta possui informações sustentadas pelo contexto.")
else:
    print()
    print("FAITHFULNESS: BAIXO")
    print("A resposta possui informações que não estão sustentadas pelo contexto.")