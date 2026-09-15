import json
from datetime import datetime
from pathlib import Path

from app.evaluation.rag_evaluator import (
    evaluate_dataset,
)


# ============================================================
# DIRETÓRIOS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

RESULTS_DIR = (
    BASE_DIR
    / "data"
    / "evaluation"
    / "results"
)


# ============================================================
# SALVAR RELATÓRIO
# ============================================================

def save_evaluation_report(
    results: list[dict],
) -> Path:
    """
    Salva os resultados de uma execução da avaliação.

    Cada execução recebe um arquivo JSON próprio.

    Exemplo:

        data/evaluation/results/
            evaluation_2026-09-15_15-30-20.json
    """

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now()

    filename = (
        "evaluation_"
        f"{timestamp.strftime('%Y-%m-%d_%H-%M-%S')}"
        ".json"
    )

    output_file = RESULTS_DIR / filename

    # Calculamos as métricas médias da execução.
    metrics = calculate_summary_metrics(
        results
    )

    report = {
        "timestamp": timestamp.isoformat(),
        "total_cases": len(results),
        "metrics": metrics,
        "cases": results,
    }

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            report,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return output_file


# ============================================================
# MÉTRICAS RESUMIDAS
# ============================================================

def calculate_summary_metrics(
    results: list[dict],
) -> dict:
    """
    Calcula as métricas médias de toda a execução.

    O resultado representa a qualidade geral do RAG
    naquele experimento.
    """

    retrieval_values = [
        result["retrieval_recall_at_k"]
        for result in results
        if result["retrieval_recall_at_k"] is not None
    ]

    context_values = [
        result["context_relevance"]
        for result in results
    ]

    answer_values = [
        result["answer_relevance"]
        for result in results
    ]

    faithfulness_values = [
        result["faithfulness"]
        for result in results
    ]

    hallucination_values = [
        result["hallucination_rate"]
        for result in results
    ]

    return {
        "retrieval_recall_at_k": calculate_average(
            retrieval_values
        ),
        "context_relevance": calculate_average(
            context_values
        ),
        "answer_relevance": calculate_average(
            answer_values
        ),
        "faithfulness": calculate_average(
            faithfulness_values
        ),
        "hallucination_rate": calculate_average(
            hallucination_values
        ),
    }


def calculate_average(
    values: list[float],
) -> float | None:
    """
    Calcula a média de uma lista de valores.

    Retorna None quando não existem valores.
    """

    if not values:
        return None

    return sum(values) / len(values)


# ============================================================
# EXECUÇÃO
# ============================================================

def main():
    """
    Executa a avaliação e salva o resultado.

    Execute a partir da raiz do projeto:

        python -m app.evaluation.evaluation_report
    """

    print()
    print("=" * 60)
    print("GERANDO RELATÓRIO DE AVALIAÇÃO")
    print("=" * 60)

    results = evaluate_dataset()

    output_file = save_evaluation_report(
        results
    )

    metrics = calculate_summary_metrics(
        results
    )

    print()
    print("=== RESUMO ===")

    print(
        f"Recall@K: "
        f"{metrics['retrieval_recall_at_k']:.2f}"
    )

    print(
        f"Context Relevance: "
        f"{metrics['context_relevance']:.2f}"
    )

    print(
        f"Answer Relevance: "
        f"{metrics['answer_relevance']:.2f}"
    )

    print(
        f"Faithfulness: "
        f"{metrics['faithfulness']:.2f}"
    )

    print(
        f"Hallucination Rate: "
        f"{metrics['hallucination_rate']:.2f}"
    )

    print()
    print(
        f"Relatório salvo em:"
    )
    print(output_file)


if __name__ == "__main__":
    main()