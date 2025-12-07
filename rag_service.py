# backend/rag_service.py

import os
import logging
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient, models

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- CONFIGURATION ---

@lru_cache(maxsize=1)
def get_settings():
    """
    Loads environment variables from the .env file.
    Using lru_cache to load settings only once.
    """
    load_dotenv()
    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "qdrant_url": os.getenv("QDRANT_URL"),
        "qdrant_api_key": os.getenv("QDRANT_API_KEY"),
        "qdrant_collection_name": os.getenv("QDRANT_COLLECTION_NAME", "ai-docs"),
    }

# --- CLIENTS ---

@lru_cache(maxsize=1)
def get_qdrant_client() -> QdrantClient:
    """Initializes and returns a Qdrant client."""
    settings = get_settings()
    return QdrantClient(
        url=settings["qdrant_url"], 
        api_key=settings["qdrant_api_key"]
    )

@lru_cache(maxsize=1)
def get_embedding_model() -> OpenAIEmbeddings:
    """Initializes and returns the OpenAI embedding model."""
    settings = get_settings()
    return OpenAIEmbeddings(
        model="text-embedding-3-small", 
        api_key=settings["openai_api_key"]
    )

@lru_cache(maxsize=1)
def get_chat_model() -> ChatOpenAI:
    """Initializes and returns the OpenAI chat model."""
    settings = get_settings()
    return ChatOpenAI(
        model="gpt-4o-mini",
        api_key=settings["openai_api_key"],
        temperature=0.1,
    )

# --- EMBEDDING LOGIC ---

def embed_documentation():
    """
    Loads markdown docs, splits them, and upserts them into Qdrant.
    """
    settings = get_settings()
    qdrant_client = get_qdrant_client()
    embedding_model = get_embedding_model()
    collection_name = settings["qdrant_collection_name"]

    # 1. Check if collection exists, create if not
    try:
        qdrant_client.get_collection(collection_name=collection_name)
        logger.info(f"Collection '{collection_name}' already exists.")
    except Exception:
        logger.info(f"Collection '{collection_name}' not found. Creating...")
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=1536,  # Dimension for text-embedding-3-small
                distance=models.Distance.COSINE,
            ),
        )
        logger.info(f"Collection '{collection_name}' created.")

    # 2. Load documents from the Docusaurus directory
    # The path goes up one level from `backend` to the project root, then into `docs/docs`
    docs_path = Path(__file__).parent.parent / "docs" / "docs"
    logger.info(f"Loading documents from: {docs_path}")
    
    loader = DirectoryLoader(
        str(docs_path),
        glob="**/*.md",
        loader_cls=UnstructuredMarkdownLoader,
        show_progress=True,
    )
    documents = loader.load()

    if not documents:
        logger.warning("No documents found to embed.")
        return 0

    # 3. Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )
    chunked_documents = text_splitter.split_documents(documents)
    logger.info(f"Split {len(documents)} documents into {len(chunked_documents)} chunks.")

    # 4. Upsert chunks into Qdrant
    qdrant_client.add(
        collection_name=collection_name,
        documents=[doc.page_content for doc in chunked_documents],
        ids="auto", # Let Qdrant generate IDs
    )

    logger.info(f"Successfully embedded {len(chunked_documents)} chunks.")
    return len(chunked_documents)

# --- RAG/CHAT LOGIC ---

def ask_question(question: str) -> str:
    """
    Answers a question using a RAG pipeline.
    """
    settings = get_settings()
    qdrant_client = get_qdrant_client()
    embedding_model = get_embedding_model()
    chat_model = get_chat_model()
    collection_name = settings["qdrant_collection_name"]

    # 1. Create a retriever
    # This is a simplified retriever that just searches Qdrant
    def retrieve_context(query: str):
        search_results = qdrant_client.search(
            collection_name=collection_name,
            query_vector=embedding_model.embed_query(query),
            limit=3, # Retrieve top 3 most relevant chunks
        )
        # Format the context for the prompt
        context = "\n---\
".join([hit.payload['page_content'] for hit in search_results])
        return context

    # 2. Define the RAG prompt
    template = """
    You are a helpful assistant for the 'AI Solar System Guide'.
    Answer the user's question based only on the following context.
    If the context doesn't contain the answer, say "I'm sorry, I don't have information on that topic based on the provided documents."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    prompt = ChatPromptTemplate.from_template(template)

    # 3. Create the RAG chain
    rag_chain = (
        {"context": RunnablePassthrough() | retrieve_context, "question": RunnablePassthrough()}
        | prompt
        | chat_model
        | StrOutputParser()
    )

    # 4. Invoke the chain with the user's question
    answer = rag_chain.invoke(question)
    return answer
