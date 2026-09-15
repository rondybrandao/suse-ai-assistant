from fastapi import FastAPI, Depends 
from pydantic import BaseModel

from app.rag.assistant import Assistant
from app.api.auth import verify_firebase_token

from app.api.authorization import get_authorized_beleza_id

app = FastAPI(
    title="SUSE AI Assistant",
    description="API do assistente de IA integrada ao SUSE ERP",
    version="1.0.0",
)

assistant = Assistant()

class AssistantRequest(BaseModel):
    """
    Dados enviados pelo SUSE ERP para o assitant.
    """
    question: str

class AssistantResponse(BaseModel):
    """
    Resposta devolvida pelo Assistant.
    """
    answer: str


@app.post(
    "/api/assistant/ask",
    response_model=AssistantResponse,
)
def ask_assistant(
    request: AssistantRequest,
    user: dict = Depends(verify_firebase_token),
):
    """
    Recebe pergunta autenticada do suse erp e encaminha para assistant

    O firebase ID Token é validado antes de executar o Assistant.
    """

    uid = user["uid"]

    beleza_id = get_authorized_beleza_id(uid)

    answer = assistant.answer(
        question=request.question,
        beleza_id=beleza_id,
    )

    return AssistantResponse(
        answer=answer
    )