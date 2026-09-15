from fastapi import HTTPException
from google.cloud.firestore_v1.base_query import FieldFilter

from app.suse.firebase import get_firestore


"""
Reproduz a mesma regra de autorização do projeto suse no backend 
"""
def get_authorized_beleza_id(uid: str) -> str:
    """
    Descobre qual empresa/beleza pertence ao usuário autenticado.

    Regras:
    1. Verifica se o usuário é responsável pela beleza.
    2. Caso não seja, verifica se é colaborador.
    3. Se não possuir acesso, retorna 403.
    """

    db = get_firestore()

    # ---------------------------------------------------------
    # 1. Usuário como responsável/owner
    #
    # Equivalente ao:
    #
    # where('ownerId', '==', uid)
    #
    # usado pelo BelezaService do ERP.
    # ---------------------------------------------------------

    owner_query = (
        db.collection("beleza")
        .where(
            filter=FieldFilter(
                "ownerId",
                "==",
                uid,
            )
        )
        .limit(1)
        .stream()
    )

    for document in owner_query:
        return document.id

    # ---------------------------------------------------------
    # 2. Usuário como colaborador
    #
    # Equivalente à lógica do collectionGroup
    # existente no BelezaService do ERP.
    # ---------------------------------------------------------

    collaborator_query = (
        db.collection_group("colaboradores")
        .where(
            filter=FieldFilter(
                "id",
                "==",
                uid,
            )
        )
        .limit(1)
        .stream()
    )

    for document in collaborator_query:
        beleza_document = document.reference.parent.parent

        if beleza_document:
            return beleza_document.id

    # ---------------------------------------------------------
    # 3. Usuário autenticado, mas sem empresa autorizada
    # ---------------------------------------------------------

    raise HTTPException(
        status_code=403,
        detail="Usuário não possui acesso a uma empresa SUSE.",
    )