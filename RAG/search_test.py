from dotenv import load_dotenv
import os
import faiss
import numpy as np

from langchain_google_genai import GoogleGenerativeAIEmbeddings


load_dotenv()


print("1. Loading Gemini embeddings...")

embeddings_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("Geminie_Api_key")
)


print("2. Loading FAISS index...")

index = faiss.read_index(
    "RAG/faiss_index.bin"
)


print("3. Loading documents...")

with open(
    "RAG/documents.txt",
    "r",
    encoding="utf-8"
) as file:

    content = file.read()


documents = content.split(
    "\n\n---DOCUMENT_SEPARATOR---\n\n"
)


print("Total documents:", len(documents))


question = "Why does a CNC machine have high vibration?"


print("\n4. Creating question embedding...")

question_vector = embeddings_model.embed_query(
    question
)


question_vector = np.array(
    [question_vector],
    dtype="float32"
)


print("5. Searching FAISS...")

distances, indices = index.search(
    question_vector,
    3
)


print("\nRelevant Knowledge Found:\n")


for i, index_number in enumerate(indices[0]):

    print("=" * 60)

    print(f"Result {i + 1}")

    print("=" * 60)

    print(documents[index_number])

    print("Distance:", distances[0][i])