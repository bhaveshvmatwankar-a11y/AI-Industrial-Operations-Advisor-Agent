from dotenv import load_dotenv
import os
import faiss
import numpy as np

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from text_splitter import chunks


load_dotenv()


print("1. Loading Gemini embeddings...")

embeddings_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("Geminie_Api_key")
)


print("2. Preparing documents...")

documents = [
    chunk.page_content
    for chunk in chunks
]

print(f"Total documents: {len(documents)}")


print("3. Creating Gemini embeddings...")

vectors = embeddings_model.embed_documents(
    documents
)


print("4. Converting vectors to NumPy format...")

vectors = np.array(
    vectors,
    dtype="float32"
)


print("Vector shape:", vectors.shape)


print("5. Creating FAISS index...")

dimension = vectors.shape[1]

index = faiss.IndexFlatL2(
    dimension
)


print("6. Adding vectors to FAISS...")

index.add(
    vectors
)


print("7. Saving FAISS index...")

faiss.write_index(
    index,
    "RAG/faiss_index.bin"
)


print("8. Saving documents...")

with open(
    "RAG/documents.txt",
    "w",
    encoding="utf-8"
) as file:

    for document in documents:

        file.write(
            document
            + "\n\n---DOCUMENT_SEPARATOR---\n\n"
        )


print("\nFAISS vector database created successfully!")

print("Total vectors stored:", index.ntotal)