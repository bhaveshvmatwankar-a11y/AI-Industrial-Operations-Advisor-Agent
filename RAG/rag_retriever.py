from dotenv import load_dotenv
import os
import faiss
import numpy as np
import streamlit as st

from langchain_google_genai import GoogleGenerativeAIEmbeddings


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# GET GEMINI API KEY
# --------------------------------------------------

api_key = os.getenv("Geminie_Api_key")

if not api_key:
    try:
        api_key = st.secrets["Geminie_Api_key"]
    except Exception:
        api_key = None


if not api_key:
    raise RuntimeError(
        "Gemini API key not configured. "
        "Add Geminie_Api_key to Streamlit Secrets "
        "or configure it in the local .env file."
    )


# --------------------------------------------------
# LOAD GEMINI EMBEDDING MODEL
# --------------------------------------------------

print("Loading Gemini embedding model...")

embeddings_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=api_key
)


# --------------------------------------------------
# LOAD FAISS INDEX
# --------------------------------------------------

print("Loading FAISS index...")

index = faiss.read_index(
    "RAG/faiss_index.bin"
)


# --------------------------------------------------
# LOAD KNOWLEDGE DOCUMENTS
# --------------------------------------------------

print("Loading knowledge documents...")

with open(
    "RAG/documents.txt",
    "r",
    encoding="utf-8"
) as file:

    content = file.read()


documents = [
    document
    for document in content.split(
        "\n\n---DOCUMENT_SEPARATOR---\n\n"
    )
    if document.strip()
]


# --------------------------------------------------
# RAG RETRIEVAL TOOL
# --------------------------------------------------

def retrieve_knowledge(
    question: str,
    k: int = 3
) -> str:
    """
    Search the industrial knowledge base for relevant
    maintenance information.
    """

    print("\n===== RAG TOOL USED =====")

    question_vector = embeddings_model.embed_query(
        question
    )

    question_vector = np.array(
        [question_vector],
        dtype="float32"
    )

    distances, indices = index.search(
        question_vector,
        k
    )

    retrieved_documents = []

    for index_number in indices[0]:

        retrieved_documents.append(
            documents[index_number]
        )

    context = "\n\n".join(
        retrieved_documents
    )

    return context