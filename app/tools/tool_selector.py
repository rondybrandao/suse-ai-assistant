from collections.abc import Callable
from typing import Any

from app.tools.definitions import ERP_TOOL_DEFINITIONS


class ToolSelector:
    """
    Registro e seleção das ferramentas ERP.
    """

    def __init__(
        self,
        erp_tools,
    ):
        self.erp_tools = erp_tools

        self.tools: dict[str, dict[str, Any]] = {
            "count_cancelled_os": {
                "definition": ERP_TOOL_DEFINITIONS[0],
                "function": (
                    self.erp_tools.count_cancelled_os
                ),
            },
            "count_finalized_os": {
                "definition": ERP_TOOL_DEFINITIONS[1],
                "function": (
                    self.erp_tools.count_finalized_os
                ),
            },
            "count_waiting_approval_os": {
                "definition": ERP_TOOL_DEFINITIONS[2],
                "function": (
                    self.erp_tools.count_waiting_approval_os
                ),
            },
        }

    def select(
        self,
        question: str,
    ) -> Callable[..., Any] | None:
        question = question.lower()

        if (
            "os cancelada" in question
            or "os canceladas" in question
        ):
            return self.tools[
                "count_cancelled_os"
            ]["function"]

        if (
            "os finalizada" in question
            or "os finalizadas" in question
        ):
            return self.tools[
                "count_finalized_os"
            ]["function"]

        if (
            "aguardando aprovação" in question
            or "aguardando aprovacao" in question
        ):
            return self.tools[
                "count_waiting_approval_os"
            ]["function"]

        return None

    def get_definitions(self):
        """
        Retorna as definições das ferramentas
        disponíveis para o LLM.
        """

        return [
            tool["definition"]
            for tool in self.tools.values()
        ]