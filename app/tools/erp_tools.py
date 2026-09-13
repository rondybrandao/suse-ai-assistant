from typing import Any

from app.suse.os_service import OsService


class ErpTools:
    """
    Ferramentas que permitem ao AI Assistant
    consultar dados do SUSE ERP.
    """

    def __init__(self):
        self.os_service = OsService()

    def get_cancelled_os(
        self,
        beleza_id: str,
    ) -> dict[str, Any]:
        """
        Retorna informações sobre as OS canceladas.
        """

        os_list = self.os_service.listar_canceladas(
            beleza_id
        )

        return {
            "total": len(os_list),
            "status": "CANCELADO",
            "os": [
                {
                    "id": os.get("id"),
                    "numero": os.get("numero"),
                    "cliente": os.get(
                        "cliente",
                        {}
                    ).get("nome"),
                    "pagamento_pendente": os.get(
                        "pendencias",
                        {}
                    ).get("pagamento"),
                }
                for os in os_list
            ],
        }

    def count_cancelled_os(
    self,
    beleza_id: str,
    ) -> int:
        """
        Retorna somente a quantidade de OS canceladas.
        """

        os_list = self.os_service.listar_canceladas(
            beleza_id
        )

        return len(os_list)

    def count_finalized_os(
    self,
    beleza_id: str,
    ) -> int:
        """
        Retorna somente a quantidade de OS finalizadas.
        """

        os_list = self.os_service.listar_por_status(
            beleza_id,
            "FINALIZADO",
        )

        return len(os_list)

    def count_waiting_approval_os(
    self,
    beleza_id: str,
    ) -> int:
        """
        Retorna somente a quantidade de OS
        aguardando aprovação.
        """

        os_list = self.os_service.listar_por_status(
            beleza_id,
            "AGUARDANDO_APROVACAO",
        )

        return len(os_list)