from app.rag.router import route_question
from app.rag.generator import generate_answer
from app.rag.embeddings import generate_embeddings
from app.rag.qdrant_client import search_similar
from app.tools.tool_selector import ToolSelector


class Assistant:
    """
    Orquestra o atendimeto do SUSE AI Assistant.
    Decide se a pergunta deve utilizar o ERP ou RAG
    """

    def __init__(self):
        self.erp_tools = ToolSelector()

    def answer(
        self,
        question: str,
        beleza_id: str,
    ):
        """
        Processa uma pergunta e direciona para fonte adequada
        """

        route = route_question(
            question
        )

        if route == "erp":
            return self._answer_from_erp(
                question,
                beleza_id,
            )

        return self._answer_from_rag(
            question
        )

    def _answer_from_erp(
    self,
    question: str,
    beleza_id: str,
    ):
        tool = self.tool_selector.select(
            question
        )

        if tool is None:
            return (
                "Não encontrei uma ferramenta ERP "
                "para essa pergunta."
            )

        total = tool(beleza_id)

        contexts = [
            f"O resultado da consulta ERP é {total}."
        ]

        return generate_answer(
            question,
            contexts,
        )

    def _answer_from_rag(
        self,
        question: str,
    ):
        """
        Mantém o fluxo RAG para perguntas
        relacionadas à documentação.
        """

        # Transforma a perguta em embedding
        query_embedding = generate_embeddings(
            [question]
        )[0]

        # Busca os chunks semanticamente mais proximos
        results = search_similar(
            query_embedding,
            limit=5,
        )

        # Extrai o texto armazenado no payload do Qdrant
        contexts = [
            result.payload["text"]
            for result in results
        ]

        if not contexts:
            return (
                "Não encontrei informações suficiente na documentação"
            )

        return generate_answer(
            question,
            contexts,
        )



        