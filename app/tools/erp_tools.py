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