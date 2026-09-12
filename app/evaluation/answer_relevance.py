import re
import unicodedata


def normalize_text(text):
    """
    Normaliza um texto para facilitar a comparação
    entre palavras com pequenas variações.

    Exemplos:

    "finalizada" -> "finalizada"
    "Finalização" -> "finalizacao"
    "FECHAMENTO" -> "fechamento"
    """

    text = text.lower()

    # Remove acentos.
    text = unicodedata.normalize(
        "NFD",
        text,
    )

    text = "".join(
        character
        for character in text
        if unicodedata.category(character) != "Mn"
    )

    return text


def keyword_matches(
    keyword,
    text,
):
    """
    Verifica se a palavra-chave ou uma de suas
    variações aparece no texto.

    Trabalhamos com grupos de palavras relacionadas
    para evitar depender de uma correspondência
    literal.
    """

    keyword = normalize_text(keyword)
    text = normalize_text(text)

    variations = {
        "fechamento": [
            "fechamento",
            "finalizacao",
            "finalizado",
            "finalizada",
            "encerramento",
        ],
        "finalizacao": [
            "finalizacao",
            "finalizado",
            "finalizada",
            "fechamento",
            "encerramento",
        ],
        "finalizado": [
            "finalizado",
            "finalizada",
            "finalizacao",
            "fechamento",
            "encerramento",
        ],
        "finalizada": [
            "finalizada",
            "finalizado",
            "finalizacao",
            "fechamento",
            "encerramento",
        ],
        "pagamento": [
            "pagamento",
            "pagar",
            "pago",
        ],
        "processado": [
            "processado",
            "processada",
            "processar",
        ],
    }

    possible_matches = variations.get(
        keyword,
        [keyword],
    )

    words = re.findall(
        r"\b\w+\b",
        text,
    )

    return any(
        variation in words
        for variation in possible_matches
    )


def calculate_answer_relevance(
    question,
    answer,
    relevant_keywords,
):
    """
    Calcula a relevância da resposta.

    A função:

    1. Identifica quais palavras relevantes
       aparecem na pergunta.

    2. Procura essas palavras ou suas variações
       na resposta.

    3. Calcula a proporção de palavras relevantes
       encontradas na resposta.
    """

    relevant_question_keywords = [
        keyword
        for keyword in relevant_keywords
        if keyword_matches(
            keyword,
            question,
        )
    ]

    if not relevant_question_keywords:
        return 0.0

    matches = sum(
        1
        for keyword in relevant_question_keywords
        if keyword_matches(
            keyword,
            answer,
        )
    )

    return matches / len(
        relevant_question_keywords
    )