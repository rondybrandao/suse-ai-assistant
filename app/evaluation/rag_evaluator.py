import json
from pathlib import Path

from app.evaluation.retrieval import (
    calculate_recall_at_k,
)

from app.evaluation.context_relevance import (
    calculate_context_relevance,
)

from app.evaluation.answer_relevance import (
    calculate_answer_relevance,
)

from app.evaluation.hallucination import (
    calculate_hallucination_rate,
)

from app.evaluation.faithfulness_LLM_grounding_as_ajudge import (
    FaithfulnessEvaluator,
)


# ============================================================
# DATASET DE AVALIAÇÃO
# ============================================================

# O arquivo está em:
#
# data/evaluation/rag_eval.json
#
# parents[2] sobe de:
#
# app/evaluation/
#       ↓
# app/
#       ↓
# raiz do projeto
BASE_DIR = Path(__file__).resolve().parents[2]

EVALUATION_FILE = (
    BASE_DIR
    / "data"
    / "evaluation"
    / "rag_eval.json"
)


# ============================================================
# PALAVRAS-CHAVE DA AVALIAÇÃO
# ============================================================

# Estas palavras pertencem à avaliação atual sobre
# fechamento/finalização de uma Ordem de Serviço.
#
# Elas são usadas pelas métricas heurísticas de
# Context Relevance e Answer Relevance.
#
# Não colocamos essas palavras dentro do rag_eval.json
# porque elas fazem parte da configuração da avaliação,
# não dos dados produzidos pelo RAG.
CONTEXT_RELEVANT_KEYWORDS = [
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


ANSWER_RELEVANT_KEYWORDS = [
    "fechamento",
    "finalização",
    "finalizado",
    "finalizada",
    "encerramento",
    "pagamento",
    "processado",
]


def load_evaluation_dataset():
    """
    Carrega o dataset JSON.

    O JSON contém os casos que queremos avaliar,
    incluindo pergunta, contexto recuperado,
    resposta gerada e IDs recuperados.
    """

    with open(
        EVALUATION_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


def evaluate_retrieval(item):
    """
    Avalia a qualidade do Retrieval.

    Comparamos:

        retrieved_ids
              X
        expected_ids

    A métrica utilizada é Recall@K, implementada
    no módulo retrieval.py.
    """

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
    Avalia se os contextos recuperados são relevantes
    para o assunto da pergunta.

    A implementação da métrica está em:

        app/evaluation/context_relevance.py

    Este método apenas fornece os dados necessários.
    """

    retrieved_contexts = item.get(
        "retrieved_context",
        [],
    )

    return calculate_context_relevance(
        retrieved_contexts,
        CONTEXT_RELEVANT_KEYWORDS,
    )


def evaluate_answer_relevance(item):
    """
    Avalia se a resposta gerada responde ao assunto
    da pergunta.

    A implementação está em:

        app/evaluation/answer_relevance.py

    Novamente, o rag_evaluator apenas orquestra.
    """

    question = item.get(
        "question",
        "",
    )

    generated_answer = item.get(
        "generated_answer",
        "",
    )

    return calculate_answer_relevance(
        question,
        generated_answer,
        ANSWER_RELEVANT_KEYWORDS,
    )


def evaluate_faithfulness(
    item,
    faithfulness_evaluator,
):
    """
    Avalia Faithfulness utilizando o modelo NLI local.

    Diferentemente das métricas de keywords,
    aqui usamos o modelo especializado que você baixou:

        mDeBERTa-v3-base-grounding-multilingual

    O modelo verifica se as afirmações da resposta
    são sustentadas pelo contexto recuperado.
    """

    generated_answer = item.get(
        "generated_answer",
        "",
    )

    retrieved_contexts = item.get(
        "retrieved_context",
        [],
    )

    # O modelo recebe todo o contexto recuperado.
    context = "\n\n".join(
        retrieved_contexts
    )

    return faithfulness_evaluator.evaluate(
        context,
        generated_answer,
    )


def evaluate_hallucination(
    faithfulness_result,
):
    """
    Calcula a taxa de possíveis alucinações a partir
    das afirmações avaliadas pelo NLI.

    Uma afirmação que não é suportada pelo contexto
    é considerada não suportada.
    """

    evaluations = []

    for claim in faithfulness_result["claims"]:

        evaluations.append(
            {
                "supported": (
                    claim["label"] == "entailment"
                )
            }
        )

    return calculate_hallucination_rate(
        evaluations
    )


def evaluate_case(
    item,
    faithfulness_evaluator,
):
    """
    Executa todas as métricas para um caso.

    Observe que este método não implementa nenhuma
    métrica.

    Ele somente conecta os módulos existentes:

        retrieval.py
        context_relevance.py
        answer_relevance.py
        faithfulness_LLM_grounding_as_ajudge.py
        hallucination.py
    """

    retrieval_score = evaluate_retrieval(
        item
    )

    context_score = evaluate_context_relevance(
        item
    )

    answer_score = evaluate_answer_relevance(
        item
    )

    faithfulness_result = evaluate_faithfulness(
        item,
        faithfulness_evaluator,
    )

    hallucination_score = evaluate_hallucination(
        faithfulness_result
    )

    return {
        "question": item["question"],
        "retrieval_recall_at_k": retrieval_score,
        "context_relevance": context_score,
        "answer_relevance": answer_score,
        "faithfulness": (
            faithfulness_result[
                "faithfulness_score"
            ]
        ),
        "hallucination_rate": hallucination_score,
        "faithfulness_details": faithfulness_result,
    }


def evaluate_dataset():
    """
    Executa a avaliação de todos os casos do JSON.

    O modelo NLI é carregado uma única vez.

    Isso é importante porque o modelo possui
    aproximadamente 350 MB.
    """

    dataset = load_evaluation_dataset()

    # Carregamos o modelo apenas uma vez.
    faithfulness_evaluator = FaithfulnessEvaluator()

    results = []

    for item in dataset:

        result = evaluate_case(
            item,
            faithfulness_evaluator,
        )

        results.append(result)

    return results


def print_report(results):
    """
    Exibe os resultados da avaliação.

    A lógica das métricas continua nos arquivos
    especializados. Aqui somente apresentamos os resultados.
    """

    print()
    print("=" * 60)
    print("AVALIAÇÃO RAG - SUSE AI ASSISTANT")
    print("=" * 60)

    for index, result in enumerate(
        results,
        start=1,
    ):

        print()
        print("-" * 60)
        print(f"CASO {index}")
        print("-" * 60)

        print(
            f"Pergunta: "
            f"{result['question']}"
        )

        retrieval_score = (
            result["retrieval_recall_at_k"]
        )

        if retrieval_score is None:

            print(
                "Recall@K: não definido"
            )

        else:

            print(
                f"Recall@K: "
                f"{retrieval_score:.2f}"
            )

        print(
            f"Context Relevance: "
            f"{result['context_relevance']:.2f}"
        )

        print(
            f"Answer Relevance: "
            f"{result['answer_relevance']:.2f}"
        )

        print(
            f"Faithfulness: "
            f"{result['faithfulness']:.2f}"
        )

        print(
            f"Hallucination Rate: "
            f"{result['hallucination_rate']:.2f}"
        )

        print()
        print("Claims avaliadas:")

        for claim in result[
            "faithfulness_details"
        ]["claims"]:

            status = (
                "SUPPORTED"
                if claim["label"] == "entailment"
                else "NOT_SUPPORTED"
            )

            print(
                f"- {status}: "
                f"{claim['claim']}"
            )


def main():
    """
    Ponto de entrada da avaliação.

    Execute a partir da raiz do projeto:

        python -m app.evaluation.rag_evaluator
    """

    results = evaluate_dataset()

    print_report(results)


if __name__ == "__main__":
    main()