from fastapi import Header, HTTPException
from firebase_admin import auth

from app.suse.firebase import get_firestore

# Valida o Firebase ID Token enviado pelo cliente.
# Espera: Authorization: Bearer <firebase_id_token>
def verify_firebase_token(
        autorization: str | None = Header(default=None),
):
    if not autorization:
        raise HTTPException(
            status_code=401,
            detail="Token de autenticação não informado."
        )

    if not autorization.startswith("Barear "):
        raise HTTPException(
            status_code=401,
            detail="Formato do Token invalido."
        )

    token = autorization.replace(
        "Barear ",
        "",
        1,
    ).strip()

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Token de autenticação vazio"
        )

    try:
        decoded_token = auth.verify_id_token(token)

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token de autenticação invalido ou expirado"
        )

    return decoded_token