from app.rag.embeddings import generate_embeddings
from app.rag.qdrant_client import search_similar


def test_compare_retrieval_queries():
    queries = [
        "Como funciona o processo de finalização?",
        "Como funciona a finalização de uma OS?",
        "O que acontece quando uma OS é marcada como FINALIZADO?",
        "Como funciona o fechamento de uma OS?",
        "O que acontece na finalização da OS?",
    ]

    for query in queries:
        print("\n" + "=" * 80)
        print(f"QUERY: {query}")
        print("=" * 80)

        # Gera o embedding da pergunta
        embedding = generate_embeddings([query])[0]

        # Busca os 5 chunks semanticamente mais próximos
        results = search_similar(
            embedding,
            limit=5,
        )

        for position, result in enumerate(results, start=1):
            print(f"\n--- TOP {position} ---")
            print(f"ID: {result.id}")
            print(f"SCORE: {result.score}")
            print(
                f"TEXTO:\n"
                f"{result.payload.get('text', '')[:500]}"
            )