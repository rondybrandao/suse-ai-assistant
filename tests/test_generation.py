from app.rag.embeddings import generate_embeddings
from app.rag.qdrant_client import search_similar
from app.rag.generator import generate_answer

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

print()
print("========================================")
print("GERAÇÃO DA RESPOSTA")
print("========================================")

print(f"Pergunta: {query}")

print()
print("Contextos utilizados:")
print("----------------------------------------")

for index, context in enumerate(contexts, start=1):
    print(f"\nContexto {index}:")
    print(context)

print()
print("========================================")
print("RESPOSTA GERADA")
print("========================================")

print(answer)