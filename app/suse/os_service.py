from typing import Any

from app.suse.firebase import get_firestore

class OsService:
    """
    Serviço Python para consulta das OS do SUSE ERP.

    Este serviço não substitui o OsService Angular.
    Ele fornece somente os dados necessários ao AI Assistant.
    """

    def __init__(self):
        self.db = get_firestore()

    def _collection(self, beleza_id: str):
        """
        retorna a coleção do OS de uma empresa/salao
        """

        return self.db.collection(
            f"beleza/{beleza_id}/os"
        )

    def listar(
        self,
        beleza_id:str,
    ) -> list[dict[str, Any]]:
        """
        Lista as os de um salão ou clinica de beleza
        """

        documents = self._collection(
            beleza_id
        ).stream()

        return [
            {
                "id": document.id,
                **document.to_dict(),
            }
            for document in documents
        ]

    def obter(
        self,
        beleza_id: str,
        os_id: str
    ) -> dict[str, Any] | None:
        """
        Busca uma os específica.
        """

        document = (
            self._colection(beleza_id)
            .document(os_id)
            .get()
        )

        if not document.exists:
            return None

        return {
            "id": document.id,
            **document.to_dict(),
        }

    def listar_por_status(
        self,
        beleza_id: str,
        status: str,
    ) -> list[dict[str, Any]]:
        """
        Lista OS filtrando pelo status.
        """

        documents = (
            self._collection(beleza_id)
            .where(
                "status",
                "==",
                status,
            )
            .stream()
        )

        return [
            {
                "id": document.id,
                **document.to_dict(),
            }
            for document in documents
        ]

    def listar_por_pagamento_pendente(
    self,
    beleza_id: str,
    ) -> list[dict[str, Any]]:
        """
        Lista OS finalizadas que ainda possuem
        pagamento pendente.
        """

        documents = (
            self._collection(beleza_id)
            .where(
                "status",
                "==",
                "FINALIZADO",
            )
            .where(
                "pendencias.pagamento",
                "==",
                True,
            )
            .stream()
        )

        return [
            {
                "id": document.id,
                **document.to_dict(),
            }
            for document in documents
        ]