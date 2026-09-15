from app.rag.generator import generate_answer
from app.tools.llm_tool_caller import LlmToolCaller


class Assistant:
    """
    Orquestra o atendimento do SUSE AI Assistant.

    O LLM decide quais ferramentas devem ser utilizadas:
    - ferramentas do ERP
    - ferramenta de busca na documentação (RAG)
    - ou ambas
    """

    def __init__(self):
        # Responsável pelo tool calling com o LLM.
        self.llm_tool_caller = LlmToolCaller()

    def answer(
        self,
        question: str,
        beleza_id: str,
    ):
        """
        Processa a pergunta utilizando o fluxo de
        tool calling.

        O LLM decide se precisa consultar:
        - ERP
        - RAG
        - ERP + RAG
        """

        tool_result = self.llm_tool_caller.call_with_tools(
            question,
            beleza_id,
        )

        #print("\n=== RESULTADOS DAS FERRAMENTAS ===")
        #print(tool_result)

        # Se o LLM respondeu diretamente sem utilizar
        # nenhuma ferramenta, retornamos a resposta.
        if not tool_result["results"]:
            return tool_result["response"]

        contexts = []

        for item in tool_result["results"]:
            result = item.get("result")

            if not result:
                continue

            # Resultado da ferramenta RAG.
            if item["tool"] == "search_suse_documentation":
                contexts.extend(
                    result.get("contexts", [])
                )

            # Resultado de ferramentas ERP.
            else:
                contexts.append(
                    f"Resultado da ferramenta {item['tool']}: "
                    f"{result}"
                )

        if not contexts:
            return (
                "Não foi possível obter informações "
                "para responder à pergunta."
            )

        #print("\n=== CONTEXTOS ENVIADOS AO GEMINI ===")

        #for i, context in enumerate(contexts, start=1):
        #    print(f"\n--- CONTEXTO {i} ---")
        #    print(context)

        # O Gemini transforma os resultados das ferramentas
        # em uma resposta final para o usuário.
        return generate_answer(
            question,
            contexts,
        )