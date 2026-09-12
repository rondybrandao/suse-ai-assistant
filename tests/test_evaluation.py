import json

from app.evaluation.retrieval import calculate_recall_at_k

from app.evaluation.context_relevance import (
    calculate_context_relevance,
)

from app.evaluation.answer_relevance import (
    calculate_answer_relevance,
)

from app.evaluation.faithfulness import (
    calculate_faithfulness,
)


# Caminho do dataset de avaliação.
EVALUATION_FILE = "data/evaluation/rag_eval.json"

def load_evaluation_dataset():
    """
    Carrega o arquivo JSON e transforma seu conteúdo
    em uma lista de dicionários Python.
    """

    with open(
        EVALUATION_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)

def evaluate_retrieval(item):
    """
    Avalia o Retrieval de uma pergunta.

    Para isso precisamos saber quais chunks são
    considerados relevantes para a pergunta.
    """

    # Embutimos temporariamente o ID esperado no
    # próprio registro da pergunta.
    expected_ids = item.get(
        "expected_ids",
        [],
    )

    retrieved_ids = item.get(
        "retrieved_ids",
        [],
    )

    if not expected_ids:
            return None

    return calculate_recall_at_k(
        retrieved_ids,
        expected_ids,
    )


def evaluate_context_relevance(item):
    """
    Calcula a relevância dos contextos recuperados.

    A função atual utiliza palavras-chave como
    uma heurística simples de avaliação.
    """

    contexts = item.get(
        "retrieved_context",
        []
    )

    # Palavras relacionadas ao assunto que estamos
    # avaliando neste primeiro dataset.
    relevant_keywords = [
        "finalizado",
        "finalização",
        "fechamento",
        "encerramento",
        "histórico",
        "financeiro",
        "metas",
        "CRM",
        "pagamento",
    ]

    return calculate_context_relevance(
        contexts,
        relevant_keywords,
    )


def evaluate_answer_relevance(item):
    """
    Calcula a relevância da resposta gerada.

    A métrica verifica se palavras importantes
    presentes na pergunta também aparecem
    na resposta.

    Esta implementação é uma heurística simples
    baseada em palavras-chave.
    """

    question = item["question"]

    answer = item.get(
        "generated_answer",
        "",
    )

    relevant_keywords = [
        "fechamento",
        "finalização",
        "finalizado",
        "finalizada",
        "encerramento",
        "pagamento",
        "processado",
    ]

    return calculate_answer_relevance(
        question,
        answer,
        relevant_keywords,
    )


def  evaluate_faithfulness(item):
    """
    Avalia se as afirmações da resposta
    são sustentadas pelos contextos recuperados.

    Retorna:

        score:
            percentual de afirmações sustentadas.

        evaluations:
            lista contendo cada afirmação
            e seu respectivo status.
    """

    answer = item.get(
        "generate_answer",
        "",
    )

    contexts = item.get(
        "retrieved_context",
        [],
    )

    score, evaluations = calculate_faithfulness(
        answer,
        contexts,
    )

    return score, evaluations



def main():
    """
    Executa todas as métricas de avaliação
    para as perguntas do dataset.
    """

    dataset = load_evaluation_dataset()

    print()
    print("========================================")
    print("AVALIAÇÃO DO RAG")
    print("========================================")

    for index, item in enumerate(
        dataset,
        start=1,
    ):

        question = item["question"]

        # ----------------------------------------
        # RETRIEVAL
        # ----------------------------------------

        retrieval_score = evaluate_retrieval(
            item
        )

        # ----------------------------------------
        # CONTEXT RELEVANCE
        # ----------------------------------------

        context_score = evaluate_context_relevance(
            item
        )

        # ----------------------------------------
        # ANSWER RELEVANCE
        # ----------------------------------------

        answer_score = evaluate_answer_relevance(
            item
        )

        # ----------------------------------------
        # FAITHFULNESS
        # ----------------------------------------

        faithfulness_score, evaluations = (
            evaluate_faithfulness(item)
        )

        print()
        print("----------------------------------------")
        print(f"Pergunta {index}")
        print("----------------------------------------")

        print(
            f"Pergunta: {question}"
        )

        if retrieval_score is None:

            print(
                "Recall@5: não definido"
            )

        else:

            print(
                f"Recall@5: "
                f"{retrieval_score:.2f}"
            )

        print(
            f"Context Relevance: "
            f"{context_score:.2f}"
        )

        print(
            f"Answer Relevance: "
            f"{answer_score:.2f}"
        )

        print(
            f"Faithfulness: "
            f"{faithfulness_score:.2f}"
        )

        # ----------------------------------------
        # CLAIMS
        # ----------------------------------------

        print()
        print("Claims avaliadas:")

        for claim in evaluations:

            status = (
                "SUPPORTED"
                if claim["supported"]
                else "NOT_SUPPORTED"
            )

            print(
                f"- {status}: "
                f"{claim['claim']}"
            )



if __name__ == "__main__":
    main()