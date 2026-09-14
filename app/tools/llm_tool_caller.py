import json
from typing import Any

from huggingface_hub import InferenceClient

from app.config import settings
from app.tools.definitions import (
    ERP_TOOL_DEFINITIONS,
    RAG_TOOL_DEFINITIONS,
)
from app.tools.erp_tools import ErpTools
from app.tools.rag_tools import RagTools


MODEL_ID = "Qwen/Qwen3-4B-Thinking-2507"
PROVIDER = "featherless-ai"

class LlmToolCaller:
    """
    Executa o ciclo de tool calling entre o LLm 
    e as ferramentas do ERP
    O LLM pode escolher uma ou varias ferramentas
    """

    def __init__(self):
        self.client = InferenceClient(
            provider=PROVIDER,
            api_key=settings.hf_token,
        )

        self.erp_tools = ErpTools()
        self.rag_tools = RagTools()

        # Mapeia o nome informado pelo LLM
        self.tools = {
            "count_cancelled_os": (
                self.erp_tools.count_cancelled_os
            ),
            "count_finalized_os": (
                self.erp_tools.count_finalized_os
            ),
            "count_waiting_approval_os": (
                self.erp_tools.count_waiting_approval_os
            ),
            "search_suse_documentation": (
                self.rag_tools.search_suse_documentation
            ),
        }

    def _get_tool_definitions(self):
        """
        Converte as definições internas para p formato
        esperado pela API de tool calling.
        """

        definitions = (
            ERP_TOOL_DEFINITIONS
            + RAG_TOOL_DEFINITIONS
        )

        return [
            {
                "type": "function",
                "function": definition,
            }
            for definition in definitions
        ]

    def _execute_tool(
            self,
            tool_call,
            beleza_id: str,
            original_question: str,
    ) -> dict[str, Any]:

        """
        Executa no Python a ferramenta solicitada pelo LLM.

        O LLM apenas escolhe a ferramenta.
        
        Para o RAG usamos a pergunta original do usuário,
        evitando que uma reformulação do LLM prejudique
        a recuperação semântica.

        """

        tool_name = tool_call.function.name

        try:
            arguments = json.loads(
                tool_call.function.arguments or "{}"
            )
        except json.JSONDecodeError:
            return {
                "tool": tool_name,
                "result": None,
                "error": "Argumentos invalidos"
            }

        tool = self.tools.get(tool_name)

        if tool is None:
            return {
                "tool": tool_name,
                "result": None,
                "error": (
                    "A ferramenta solicitada não esta disponivel"
                ),
            }

        # RAG recebe a pergunta original.
        if tool_name == "search_suse_documentation":
            result = tool(original_question)
        else:
            result = tool(
                beleza_id,
                **arguments,
            )

        return {
            "tool": tool_name,
            "result": result,
            "error": None,
        }

    def call_with_tools(
        self,
        question: str,
        beleza_id: str,
    ) -> dict[str, Any]:
        """
        Envia a pergunta ao LLM e executa todas as
        ferramentas solicitadas.

        """

        tools = self._get_tool_definitions()

        messages = [
            {
                "role": "user",
                "content": question,
            }
        ]

        response = self.client.chat.completions.create(
            model=MODEL_ID,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # O LLM conseguiu responder sem precisar
        # consultar nenhuma ferramenta.
        if not message.tool_calls:
            return {
                "tool_calls": [],
                "results": [],
                "response": message.content or "",
            }

        results = []

        # executa cada ferramenta solicitada pelo LLM.
        for tool_call in message.tool_calls:
            result = self._execute_tool(
                tool_call,
                beleza_id,
                question,
            )

            results.append(result)

        return {
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments,
                }
                for tool_call in message.tool_calls
            ],
            "results": results,
            "response": None,
        }



