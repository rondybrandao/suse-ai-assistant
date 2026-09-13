from app.tools.llm_tool_caller import LlmToolCaller

BELEZA_ID = "mock-ml-suse"

def main():
    caller = LlmToolCaller()

    question = "Quantas OS estão canceladas?"

    print("=" * 60)
    print(f"Pergunta:  {question}")

    answer = caller.call(
        question,
        BELEZA_ID,
    )

    print(f"Resposta: {answer}")

if __name__ == "__main__":
    main()