from app.rag.router import route_question
from app.rag.generator import generate_answer
from app.rag.embeddings import generate_embeddings
from app.rag.qdrant_client import search_similar
from app.tools.tool_selector import ToolSelector
from app.tools.llm_tool_caller import LlmToolCaller


class Assistant:
    """
    Orquestra o atendimeto do SUSE AI Assistant.
    Decide se a pergunta deve utilizar o ERP ou RAG
    """

    def __init__(self):
        # responsavel pelo tool calling com LLM
        self.llm_tool_caller = LlmToolCaller()

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
        """
        Responde perguntas sobre dados atuais
        do ERP utilizando LLM Tool Calling
        """

        return self.llm_tool_caller.call(
            question,
            beleza_id,
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



        