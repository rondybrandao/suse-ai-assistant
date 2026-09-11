from app.rag.embeddings import generate_embeddings
from app.rag.qdrant_client import search_similar
from app.rag.generator import generate_answer

from app.evaluation.faithfulness import (
    calculate_faithfulness,
)

from app.evaluation.hallucination import (
    calculate_hallucination_rate,
)

query = "Como funciona o processo de fechamento de uma OS?"

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

# Teste negativo:
# adicionamos propositalmente uma informação
# que não está na documentação.

answer = answer + """
O sistema também envia automaticamente um e-mail
de confirmação para o cliente após a finalização da OS.
"""

score, evaluations = calculate_faithfulness(
    answer,
    contexts,
)

hallucination_rate = calculate_hallucination_rate(evaluations)

print()
print("========================================")
print("AVALIAÇÃO DE HALLUCINATION RATE")
print("========================================")

print(f"Pergunta: {query}")

print()
print("Claims:")
print("----------------------------------------")

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
print(
    f"Hallucination Rate: "
    f"{hallucination_rate:.2f}"
)

print()

if hallucination_rate == 0:
    print("HALLUCINATION RATE: OK")
else:
    print("HALLUCINATION RATE: DETECTADA")