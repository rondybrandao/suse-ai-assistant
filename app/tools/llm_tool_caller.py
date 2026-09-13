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

    def call(
        self,
        question: str,
        beleza_id: str,
    ) -> str:

        """
        Converte as definições internas 
        para o formato esperado pelo Hugging Face
        """
        tools = [
            {
                "type":"function",
                "function": definition,
            }
            for definition in ERP_TOOL_DEFINITIONS
        ]

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

        # Pegamos o primeiro tool call solicitado pelo LLM
        tool_call = message.tool_calls[0]

        tool_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        # Localiza a função correspondente
        tool = self.tools.get(tool_name)

        if tool is None:
            return (
                "A ferramenta solicitada "
                "não esta disponivel."
            )

        # Executa a ferramenta real do ERP
        result = {
            "total": tool(
                beleza_id,
                **arguments,
            )
        }

        # Adiciona a mensagem do assistant contendo a solicitação da ferramenta
        messages.append(
            message
        )

        # Adiciona o resultado da ferramenta
        # para o LLM gerar a resposta final
        messages.append(
            {
                "role":"tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": json.dumps(
                    result,
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