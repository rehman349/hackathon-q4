# backend/models.py

from pydantic import BaseModel

class ChatRequest(BaseModel):
    """
    Pydantic model for the /chat endpoint request.
    """
    question: str

class ChatResponse(BaseModel):
    """
    Pydantic model for the /chat endpoint response.
    """
    answer: str

class EmbedResponse(BaseModel):
    """
    Pydantic model for the /embed endpoint response.
    """
    message: str
    documents_embedded: int
