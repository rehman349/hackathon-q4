# backend/main.py

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.models import ChatRequest, ChatResponse, EmbedResponse
from backend.rag_service import ask_question, embed_documentation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Docs Assistant API",
    description="API for the RAG-powered documentation assistant.",
    version="1.0.0",
)

# --- CORS Configuration ---
# This allows the chat widget (on a different domain/port) to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# --- API Endpoints ---

@app.get("/", tags=["General"])
async def read_root():
    """A simple endpoint to confirm the API is running."""
    return {"message": "Welcome to the AI Docs Assistant API!"}

@app.post("/embed", response_model=EmbedResponse, tags=["Embedding"])
async def embed_docs_endpoint():
    """
    An endpoint to trigger the embedding of the documentation.
    This reads markdown files, chunks them, and stores them in Qdrant.
    """
    try:
        count = embed_documentation()
        return {"message": "Documentation embedding process completed successfully.", "documents_embedded": count}
    except Exception as e:
        logger.error(f"Error during embedding: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_with_rag(request: ChatRequest):
    """
    The main chat endpoint.
    Receives a question, uses a RAG pipeline to find an answer, and returns it.
    """
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    try:
        answer = ask_question(request.question)
        return {"answer": answer}
    except Exception as e:
        logger.error(f"Error during chat processing: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while processing your question.")

# To run this application:
# 1. Make sure you are in the `backend` directory.
# 2. Ensure your virtual environment is activated.
# 3. Run: uvicorn main:app --reload
