# Calcular alucinação de resposta
def calculate_hallucination_rate(evaluations):
    if not evaluations:
        return 0.0

    unsupported_claims = sum(
        1
        for evaluation in evaluations
        if not evaluation["supported"]
    )

    total_claims = len(evaluations)

    return unsupported_claims / total_claims