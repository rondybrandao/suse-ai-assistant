from google import genai

from app.config import settings

client = genai.Client(
    api_key=settings.gemini_api_key
)

def extract_claims(answer):
    prompt = f"""
            Extraia as afirmações factuais presentes na resposta abaixo.

            Uma afirmação (claim) deve representar uma informação
            que possa ser verificada usando uma fonte.

            Não explique nada.
            Retorne apenas uma afirmação por linha.

            Resposta:
            {answer}
            """
    interaction = client.interactions.create(
        model= settings.gemini_model,
        input=prompt,
    )

    claims = [
        line.strip()
        for line in interaction.output_text.splitlines()
        if line.strip()
    ]

    return claims


def evaluate_claim(claim, context):
    prompt = f"""
            Determine se a afirmação abaixo é sustentada pelo contexto.

            Afirmação:
            {claim}

            Contexto:
            {context}

            Responda somente com:

            SUPPORTED

            ou

            NOT_SUPPORTED
            """    

    interaction = client.interactions.create(
        model= settings.gemini_model,
        input=prompt,
    )

    result = interaction.output_text.strip().upper()

    return result == "SUPPORTED"

def calculate_faithfulness(
        answer,
        contexts,
):
    claims = extract_claims(answer)

    if not claims:
        return 0.0, []

    context_text = "\n\n".join(contexts)

    evaluations = []

    for claim in claims:
        supported = evaluate_claim(
            claim,
            context_text,
        )

        evaluations.append(
            {
                "claim": claim,
                "supported": supported,
            }
        )

    supported_claims = sum(
        1
        for evaluation in evaluations
        if evaluation["supported"]
    )

    score = supported_claims / len(claims)

    return score, evaluations