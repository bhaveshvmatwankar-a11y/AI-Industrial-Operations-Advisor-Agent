from dotenv import load_dotenv
import os
import faiss
import numpy as np

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pdf_loader import load_pdf
from document_processor import split_documents

load_dotenv()

PDF_PATH = "data/vibration_analysis.pdf"
INDEX_PATH = "RAG/pdf_faiss_index.bin"
DOCUMENT_PATH = "RAG/pdf_documents.txt"


print("1. Loading PDF...")

documents = load_pdf(PDF_PATH)

print(f"PDF pages: {len(documents)}")


print("2. Splitting PDF into chunks...")

chunks = split_documents(documents)

print(f"Total chunks: {len(chunks)}")


print("3. Loading Gemini embedding model...")

api_key = os.getenv("Geminie_Api_key")

if not api_key:
    raise RuntimeError(
        "Gemini API key not found. "
        "Check your .env file."
    )

embeddings_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=api_key
)


print("4. Creating embeddings...")

texts = [chunk.page_content for chunk in chunks]

vectors = embeddings_model.embed_documents(texts)

vectors = np.array(vectors, dtype="float32")

print("Vector shape:", vectors.shape)


print("5. Creating FAISS index...")

dimension = vectors.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(vectors)


print("6. Saving FAISS index...")

faiss.write_index(index, INDEX_PATH)


print("7. Saving PDF documents...")

with open(DOCUMENT_PATH, "w", encoding="utf-8") as file:

    for chunk in texts:

        file.write(chunk)

        file.write(
            "\n\n---DOCUMENT_SEPARATOR---\n\n"
        )


print("\nPDF FAISS vector database created successfully!")

print("Total vectors stored:", index.ntotal)