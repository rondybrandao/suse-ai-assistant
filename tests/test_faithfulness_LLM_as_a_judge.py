from app.rag.embeddings import generate_embeddings
from app.rag.qdrant_client import search_similar
from app.rag.generator import generate_answer

from app.evaluation.faithfulness_LLM_as_a_judge import (
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

answer = answer + """
O sistema também envia automaticamente um e-mail
de confirmação para o cliente após a finalização da OS.
"""

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