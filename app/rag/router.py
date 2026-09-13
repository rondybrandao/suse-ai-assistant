#versão simples deterministica
def route_question(question: str) -> str:
    """
    Decide qual fonte deve responder a pergunta.

    retorna:
        "erp" -> dados atuais do erp
        "rag" -> documentação
    """

    question = question.lower()

    erp_keywords = [
        "quantas os",
        "quantidade de os",
        "os canceladas",
        "os finalizadas",
        "os abertas",
        "aguardando aprovação",
        "pagamento pendente",
    ]

    for keyword in erp_keywords:
        if keyword in question:
            return "erp"

    return "rag"