from google import genai

from app.config import settings


client = genai.Client(
    api_key=settings.gemini_api_key
)


def calculate_faithfulness(
    answer,
    contexts,
):
    """
    Avalia se as afirmações da resposta
    são sustentadas pelos contextos recuperados.

    Retorna:

        score:
            proporção de afirmações sustentadas.

        evaluations:
            lista com cada afirmação e seu status.
    """

    context_text = "\n\n".join(
        contexts
    )

    prompt = f"""
Você é um avaliador de Faithfulness para um sistema RAG.

Analise a resposta abaixo usando EXCLUSIVAMENTE
o contexto fornecido.

Sua tarefa é:

1. Identificar cada afirmação factual da resposta.
2. Verificar se cada afirmação é sustentada pelo contexto.
3. Classificar cada afirmação como:
   - SUPPORTED
   - NOT_SUPPORTED

Uma afirmação é SUPPORTED somente quando o contexto
fornece suporte suficiente para ela.

Não considere conhecimento externo.

Responda EXATAMENTE neste formato:

CLAIM: <afirmação>
STATUS: SUPPORTED

CLAIM: <afirmação>
STATUS: NOT_SUPPORTED

Não adicione explicações.

========================================
CONTEXTO
========================================

{context_text}

========================================
RESPOSTA
========================================

{answer}
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
    )

    output = interaction.output_text.strip()

    evaluations = []

    current_claim = None

    for line in output.splitlines():

        line = line.strip()

        if line.startswith("CLAIM:"):

            current_claim = line.replace(
                "CLAIM:",
                "",
                1,
            ).strip()

        elif line.startswith("STATUS:") and current_claim:

            status = line.replace(
                "STATUS:",
                "",
                1,
            ).strip().upper()

            evaluations.append(
                {
                    "claim": current_claim,
                    "supported": status == "SUPPORTED",
                }
            )

            current_claim = None

    if not evaluations:
        return 0.0, []

    supported_claims = sum(
        1
        for evaluation in evaluations
        if evaluation["supported"]
    )

    score = supported_claims / len(
        evaluations
    )

    return score, evaluations