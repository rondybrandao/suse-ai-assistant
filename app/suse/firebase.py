import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore

from app.config import settings


def get_firestore():
    """
    Inicializa o Firebase Admin e retorna o cliente Firestore.

    A conexão é criada uma única vez.
    """

    if not firebase_admin._apps:
        cred = credentials.Certificate(
            settings.firebase_service_account
        )

        firebase_admin.initialize_app(
            cred
        )

    return firestore.client()