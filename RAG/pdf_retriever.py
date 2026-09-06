from dotenv import load_dotenv
import os
import faiss
import numpy as np

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.tools import tool

from RAG.pdf_loader import load_pdf
from RAG.document_processor import split_documents


load_dotenv()


INDEX_PATH = "RAG/pdf_faiss_index.bin"
DOCUMENT_PATH = "RAG/pdf_documents.txt"


# ==========================================================
# GEMINI EMBEDDING MODEL
# ==========================================================

api_key = os.getenv("Geminie_Api_key")

if not api_key:
    raise RuntimeError(
        "Gemini API key not found."
    )


embeddings_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=api_key
)


# ==========================================================
# ACTIVE PDF RAG DATA
# ==========================================================

index = None
documents = []


# ==========================================================
# LOAD EXISTING PDF INDEX
# ==========================================================

def load_existing_pdf_index():

    global index
    global documents

    if not os.path.exists(INDEX_PATH):
        return False

    if not os.path.exists(DOCUMENT_PATH):
        return False

    index = faiss.read_index(
        INDEX_PATH
    )

    with open(
        DOCUMENT_PATH,
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

    return True


# ==========================================================
# BUILD PDF RAG INDEX
# ==========================================================

def build_pdf_index(pdf_path):

    global index
    global documents

    print("\n===== BUILDING PDF RAG INDEX =====")

    print("Loading PDF...")

    pdf_documents = load_pdf(
        pdf_path
    )

    print(
        f"PDF pages: {len(pdf_documents)}"
    )


    print("Splitting PDF...")

    chunks = split_documents(
        pdf_documents
    )

    print(
        f"Total chunks: {len(chunks)}"
    )


    print("Creating embeddings...")

    texts = [
        chunk.page_content
        for chunk in chunks
    ]

    vectors = embeddings_model.embed_documents(
        texts
    )

    vectors = np.array(
        vectors,
        dtype="float32"
    )


    print(
        f"Vector shape: {vectors.shape}"
    )


    print("Creating FAISS index...")

    dimension = vectors.shape[1]

    new_index = faiss.IndexFlatL2(
        dimension
    )

    new_index.add(
        vectors
    )


    print("Saving FAISS index...")

    faiss.write_index(
        new_index,
        INDEX_PATH
    )


    print("Saving PDF documents...")

    with open(
        DOCUMENT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        for text in texts:

            file.write(text)

            file.write(
                "\n\n---DOCUMENT_SEPARATOR---\n\n"
            )


    # Activate newly created index
    index = new_index
    documents = texts


    print(
        "PDF RAG index built successfully."
    )

    return len(pdf_documents), len(chunks)


# ==========================================================
# INITIAL LOAD
# ==========================================================

load_existing_pdf_index()


# ==========================================================
# LANGCHAIN PDF RAG TOOL
# ==========================================================

@tool
def retrieve_pdf_knowledge(question: str) -> str:
    """
    Search the active industrial PDF knowledge base
    and return relevant information for the user's question.
    """

    if index is None or not documents:

        return (
            "No industrial PDF knowledge is currently loaded."
        )


    question_vector = (
        embeddings_model.embed_query(
            question
        )
    )

    question_vector = np.array(
        [question_vector],
        dtype="float32"
    )


    distances, indices = index.search(
        question_vector,
        3
    )


    retrieved_documents = []

    for index_number in indices[0]:

        if index_number >= 0:

            retrieved_documents.append(
                documents[index_number]
            )


    if not retrieved_documents:

        return (
            "No relevant information was found "
            "in the uploaded PDF."
        )


    context = "\n\n".join(
        retrieved_documents
    )

    return context


# ==========================================================
# DIRECT TEST
# ==========================================================

if __name__ == "__main__":

    question = (
        "What problems can vibration analysis "
        "detect in rotating machinery?"
    )

    print(
        "\n===== PDF RAG TEST ====="
    )

    result = retrieve_pdf_knowledge.invoke(
        {
            "question": question
        }
    )

    print(
        "\nQuestion:"
    )

    print(question)

    print(
        "\nRetrieved Knowledge:"
    )

    print(result)