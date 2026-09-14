from app.tools.llm_tool_caller import LlmToolCaller


BELEZA_ID = "mock-ml-suse"


def test_erp_tool_calling():
    caller = LlmToolCaller()

    result = caller.call_with_tools(
        "Quantas OS estão canceladas?",
        BELEZA_ID,
    )

    print("\n=== ERP ===")
    print(result)

    assert result["results"]
    assert any(
        item["tool"] == "count_cancelled_os"
        for item in result["results"]
    )


def test_rag_tool_calling():
    caller = LlmToolCaller()

    result = caller.call_with_tools(
        "Como funciona o processo de fechamento de uma OS?",
        BELEZA_ID,
    )

    print("\n=== RAG ===")
    print(result)

    assert result["results"]
    assert any(
        item["tool"] == "search_suse_documentation"
        for item in result["results"]
    )


def test_hybrid_tool_calling():
    caller = LlmToolCaller()

    result = caller.call_with_tools(
        (
            "Quantas OS estão finalizadas "
            "e como funciona o processo de finalização?"
        ),
        BELEZA_ID,
    )

    print("\n=== HÍBRIDO ===")
    print(result)

    tool_names = {
        item["tool"]
        for item in result["results"]
    }

    print("\nFerramentas utilizadas:")
    for tool_name in tool_names:
        print(f"- {tool_name}")

    assert "count_finalized_os" in tool_names
    assert "search_suse_documentation" in tool_names