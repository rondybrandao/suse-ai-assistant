from typing import Any

from app.rag.embeddings import generate_embeddings
from app.rag.qdrant_client import search_similar


class RagTools:
    """
    FFerramentas relacionadas à busca na documentação do SUSE
    através do RAG.
    """

    def search_suse_documentation(
        self,
        question: str,
    ) -> dict[str, Any]:
        """
        Busca na documentação de SUSE os trechos mais
        relevantes para responder uma pergunta.

        Fluxo:
            pergunta
            >> embedding
            >> busca semantica no Qdrant
            >> chunks relevantes
        """

        query_embedding = generate_embeddings(
            [question]
        )[0]

        results = search_similar(
            query_embedding,
            limit=5,
        )

        contexts = [
            results.payload["text"]
            for result in results
            if result.payload and "text" in result.payload
        ]

        return {
            "question": question,
            "total": len(contexts),
            "contexts": contexts,
        }