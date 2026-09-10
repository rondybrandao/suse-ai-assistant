from app.rag.embeddings import generate_embeddings
from app.rag.qdrant_client import search_similar

# Pergunta
query = "Como funciona o processo de fechamento de uma OS?"

# Gerar embedding da pergunta
query_embedding = generate_embeddings([query])[0]

print(f"Pergunta: {query}")
print(f"Dimensão do embedding: {len(query_embedding)}")

# Buscar chunks semelhantes
results = search_similar(
    query_embedding,
    limit=5
)

# Exibir resultado
print()
print("========================================")
print("RESULTADOS DA BUSCA SEMÂNTICA")
print("========================================")

for index, results in enumerate(results, start=1):
    print()
    print(f"Resultado: {index}")
    print(f"Score: {results.score}")
    print(f"ID: {results.id}")

    print("Texto:")
    print(results.payload["text"])