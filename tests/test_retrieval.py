from app.rag.embeddings import generate_embeddings
from app.rag.qdrant_client import search_similar

from app.evaluation.retrieval import calculate_recall_at_k

# Pergunta
query = "Como funciona o processo de fechamento de uma OS?"

# Chunk esperado
expected_ids = [29]

# Gerar embedding da pergunta
query_embedding = generate_embeddings([query])[0]

# Buscar no qdrant
results = search_similar(
    query_embedding,
    limit=5,
)

# IDs recuperados
retrieved_ids = [
    result.id
    for result in results
]

# Calcular Recall@5
recall = calculate_recall_at_k(
    retrieved_ids,
    expected_ids,
)

# Resultados
print()
print("========================")
print("Avaliação do Retrieval")
print("========================")

print(f"Pergunta: {query}")
print(f"Ids esperados: {expected_ids}")
print(f"IDs recuperados: {retrieved_ids}")
print(f"recall@5: {recall:.2f}")

if recall == 1.0:
    print()
    print("Retrieval: OK")
    print("O chunk esperado apareceu no top-5")
else:
    print()
    print("Retrieval: Falhou")
    print("O chunk esperado não foi recuperado no top-5")
