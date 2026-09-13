import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


load_dotenv()


MODEL_ID = "Qwen/Qwen3-4B-Thinking-2507"
PROVIDER = "featherless-ai"


def get_weather(
    location: str,
) -> str:
    """
    Ferramenta fictícia usada somente para testar
    o mecanismo de tool calling.
    """

    return f"Clima consultado para {location}."


def main():
    token = os.getenv("HF_TOKEN")

    if not token:
        raise RuntimeError(
            "HF_TOKEN não encontrado no arquivo .env."
        )

    client = InferenceClient(
        provider=PROVIDER,
        api_key=token,
    )

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": (
                    "Consulta o clima de uma localização."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": (
                                "Cidade e país."
                            ),
                        },
                    },
                    "required": ["location"],
                },
            },
        }
    ]

    messages = [
        {
            "role": "user",
            "content": (
                "Qual é o clima em Manaus, Brasil?"
            ),
        }
    ]

    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    message = response.choices[0].message

    print("Resposta do modelo:")
    print(message)
    print()

    if not message.tool_calls:
        print("Nenhum tool call foi gerado.")
        return

    print("Tool call detectado:")
    print("-" * 50)

    for tool_call in message.tool_calls:
        print(
            f"Função: "
            f"{tool_call.function.name}"
        )
        print(
            f"Argumentos: "
            f"{tool_call.function.arguments}"
        )


if __name__ == "__main__":
    main()