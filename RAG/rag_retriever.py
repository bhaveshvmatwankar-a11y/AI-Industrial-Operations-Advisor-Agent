from dotenv import load_dotenv
import os
import faiss
import numpy as np

from langchain_google_genai import GoogleGenerativeAIEmbeddings


load_dotenv()


print("Loading Gemini embedding model...")

embeddings_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("Geminie_Api_key")
)


print("Loading FAISS index...")

index = faiss.read_index(
    "RAG/faiss_index.bin"
)


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


def retrieve_knowledge(
    question: str,
    k: int = 3
) -> str:
    """
    Search the industrial knowledge base for relevant maintenance information.

    Use this tool when the user asks about:
    - Machine problems
    - Abnormal temperature
    - Vibration
    - Maintenance causes
    - Machine failure risks
    - Maintenance recommendations
    """

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
