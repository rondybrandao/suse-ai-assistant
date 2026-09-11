from app.rag.embeddings import generate_embeddings
from app.rag.qdrant_client import search_similar
from app.rag.generator import generate_answer

from app.evaluation.faithfulness import (
    calculate_faithfulness,
)


query = "Como funciona o processo de fechamento de uma OS?"

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

score, evaluations = calculate_faithfulness(
    answer,
    contexts,
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
print("========================================")
print("CLAIMS")
print("========================================")

for index, evaluation in enumerate(
    evaluations,
    start=1,
):
    status = (
        "SUPPORTED"
        if evaluation["supported"]
        else "NOT_SUPPORTED"
    )

    print()
    print(f"Claim {index}:")
    print(evaluation["claim"])
    print(f"Status: {status}")

print()
print("========================================")
print("RESULTADO")
print("========================================")

print(f"Faithfulness: {score:.2f}")


if score >= 0.80:
    print()
    print("FAITHFULNESS: OK")
else:
    print()
    print("FAITHFULNESS: BAIXO")