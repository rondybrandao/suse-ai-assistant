import json

from huggingface_hub import InferenceClient

from app.config import settings
from app.tools.definitions import ERP_TOOL_DEFINITIONS
from app.tools.erp_tools import ErpTools


MODEL_ID = "Qwen/Qwen3-4B-Thinking-2507"
PROVIDER = "featherless-ai"

class LlmToolCaller:
    """
    Executa o ciclo de tool calling entre o LLm 
    e as ferramentas do ERP
    """

    def __init__(self):
        self.client = InferenceClient(
            provider=PROVIDER,
            api_key=settings.hf_token,
        )

        self.erp_tools = ErpTools()

        self.tools = {
            "count_cancelled_os":
                self.erp_tools.count_cancelled_os,

            "count_finalized_os":
                self.erp_tools.count_finalized_os,

            "count_waiting_approval_os":
                self.erp_tools.count_waiting_approval_os,
        }

    def _get_tool_definitions(self):
        """
        Converte as definições internas para p formato
        esperado pelo Hugging Face
        """

        return [
            {
                "type:": "function",
                "function": definition,
            }
            for definition in ERP_TOOL_DEFINITIONS
        ]

    def _execute_tool(
            self,
            message,
            beleza_id: str,
    ):
        """
        Executa o total solicitado pelo LLM
        Retorna o nome do tool e o resultado estruturado
        """

        tool_call = message.tool_calls[0]

        tool_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        tool = self.tools.get(tool_name)

        if tool is None:
            return None

        result = tool(
            beleza_id,
            **arguments,
        )

        return {
            "tool":tool_name,
            "result": result
        }

    def call(
        self,
        question: str,
        beleza_id: str,
    ) -> str:

        """
        Converte as definições internas 
        para o formato esperado pelo Hugging Face
        """
        tools = self._get_tool_definitions()

        messages = [
            {
                "role":"user",
                "content":question,
            }
        ]

        # Primeira chamada:
        # o LLM decide se precisa utilizar uma ferramenta.
        response = self.client.chat.completions.create(
            model=MODEL_ID,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # Caso o LLM consiga responder sem ferramenta
        if not message.tool_calls:
            return message.content or ""

        tool_result = self._execute_tool(
            message,
            beleza_id
        )

        if tool_result is None:
            return (
                "A ferramenta solicitada "
                "não esta disponivel."
            )

        # Adiciona a solicitação do tool ao historico
        messages.append(
            message
        )

        # Adiciona o resultado da ferramenta
        # para o LLM gerar a resposta final
        messages.append(
            {
                "role":"tool",
                "tool_call_id": message.tool_call.id,
                "name": tool_result["tool"],
                "content": json.dumps(
                    {
                        "total":tool_result["result"]
                    },
                    ensure_ascii=False
                )
            }
        )

        # Segunda chamada:
        # o LLM recebe o resultado real do ERP
        # e transforma o resultado em linguagem natural
        final_response = (
            self.client.chat.completions.create(
                model=MODEL_ID,
                messages=messages,
                tools=tools,
                tool_choice="none"
            )
        )

        return (
            final_response
            .choices[0]
            .message
            .content
            or ""
        )


    def call_with_result(
        self,
        question: str,
        beleza_id: str,
    ) -> dict:
        """
        Executa o tool calling,mas retorna o resultado
        estruturado do ERP.
        Não faz a segunda chamada ao LLM.
        Utilizado quando Assistant precisa combinar dados ERP com contexto RAG
        """

        tools = self._get_tool_definitions()

        messages = [
            {
                "role": "user",
                "content": question,
            }
        ]

        # O LLM decide qual ferramenta utilizar
        response = self.client.chat.completions.create(
            model=MODEL_ID,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # Caso não seja necessário utilizar uma ferramenta.
        if not message.tool_calls:
            return {
                "tool": None, 
                "result": None, 
                "response": message.content or "",
            }

        tool_result = self._execute_tool(
            message,
            beleza_id,
        )

        if tool_result is None:
            return {
                "tool": None,
                "result": None,
                "response": (
                    "Aferramenta solicitada"
                    "não esta disponivel"
                ),
            }

        return {
            "tool": tool_result["tool"],
            "result": tool_result["result"],
            "response": None,
        }

