from fastapi import FastAPI 
from pydantic import BaseModel

from app.rag.assistant import Assistant

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
    beleza_id: str

class AssistantResponse(BaseModel):
    """
    Resposta devolvida pelo Assistant.
    """

    answer: str


@app.post(
    "/api/assistant/ask",
    response_model=AssistantResponse,
)
def ask_assistant(request: AssistantRequest):
    """
    Recebe pergunta do suse erp e encaminha para assistant
    """

    answer = assistant.answer(
        question=request.question,
        beleza_id=request.beleza_id,
    )

    return AssistantResponse(
        answer=answer
    )