import time
from typing import Any

from app.rag.embeddings import generate_embeddings
from app.rag.qdrant_client import search_similar


class RagTools:

    def search_suse_documentation(
        self,
        question: str,
    ) -> dict[str, Any]:

        # Tempo total da execução do RAG
        inicio_rag = time.perf_counter()

        # ---------------------------------------------------------
        # 1. Geração do embedding da pergunta
        # ---------------------------------------------------------
        inicio_embedding = time.perf_counter()

        query_embedding = generate_embeddings(
            [question]
        )[0]

        tempo_embedding = (
            time.perf_counter() - inicio_embedding
        )

        print(
            f"[TRACE] Embedding: "
            f"{tempo_embedding:.2f}s"
        )

        # ---------------------------------------------------------
        # 2. Busca dos vetores no Qdrant
        # ---------------------------------------------------------
        inicio_qdrant = time.perf_counter()

        results = search_similar(
            query_embedding,
            limit=5,
        )

        tempo_qdrant = (
            time.perf_counter() - inicio_qdrant
        )

        print(
            f"[TRACE] Qdrant: "
            f"{tempo_qdrant:.2f}s"
        )

        # ---------------------------------------------------------
        # 3. Extração dos contextos
        # ---------------------------------------------------------
        contexts = [
            result.payload["text"]
            for result in results
            if result.payload
            and "text" in result.payload
        ]

        # ---------------------------------------------------------
        # 4. Tempo total do RAG
        # ---------------------------------------------------------
        tempo_rag = (
            time.perf_counter() - inicio_rag
        )

        print(
            f"[TRACE] RAG total: "
            f"{tempo_rag:.2f}s"
        )

        return {
            "question": question,
            "total": len(contexts),
            "contexts": contexts,
        }