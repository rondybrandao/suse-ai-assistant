from app.tools.rag_tools import RagTools


def test_rag_with_original_query():
    question = (
        "Quantas OS estão finalizadas "
        "e como é esse processo de finalização?"
    )

    rag_tools = RagTools()

    result = rag_tools.search_suse_documentation(
        question
    )

    print("\n" + "=" * 80)
    print("QUERY ORIGINAL ENVIADA AO RAG")
    print("=" * 80)
    print(question)

    print("\n" + "=" * 80)
    print("RESULTADOS")
    print("=" * 80)

    print(f"Total de contextos: {result['total']}")

    for position, context in enumerate(
        result["contexts"],
        start=1,
    ):
        print(f"\n--- TOP {position} ---")
        print(context[:1000])

    assert result["total"] > 0