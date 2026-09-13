from google import genai

from app.config import settings


client = genai.Client(
    api_key=settings.gemini_api_key
)


def generate_answer(
    question,
    contexts,
):
    """
    Gera uma resposta utilizando os contextos 
    recuperados pelo RAG
    """

    context_text = "\n\n".join(
        contexts
    )

    prompt = f"""
Você é um assistente do sistema SUSE ERP.

Responda à pergunta utilizando exclusivamente
as informações presentes no contexto fornecido.

Se o contexto não contiver informação suficiente
para responder, diga que a informação não foi
encontrada na documentação.

Não invente informações.

Contexto:
{context_text}

Pergunta:
{question}

Resposta:
"""

    interaction = client.interactions.create(
        model=settings.gemini_model,
        input=prompt,
    )

    return interaction.output_text