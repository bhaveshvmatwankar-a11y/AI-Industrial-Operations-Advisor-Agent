from dotenv import load_dotenv
import os
import chromadb

from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

print("1. Creating Gemini embedding model...")

embeddings_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("Geminie_Api_key")
)

print("2. Creating test embedding...")

vector = embeddings_model.embed_query(
    "This is a test document."
)

print("3. Embedding created!")
print("Vector dimensions:", len(vector))

print("4. Creating ChromaDB client...")

client = chromadb.EphemeralClient()

print("5. Creating collection...")

collection = client.create_collection(
    name="gemini_test_collection",
    embedding_function=None
)

print("6. Adding document with Gemini vector...")

collection.add(
    ids=["test_1"],
    documents=["This is a test document."],
    embeddings=[[0.1, 0.2, 0.3]]
)

print("7. Document added successfully!")

print("Document count:", collection.count())