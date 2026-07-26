from dotenv import load_dotenv
import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("Geminie_Api_key")
)

vector = embeddings.embed_query(
    "Why does a CNC machine have high vibration?"
)

print("Embedding created successfully!")
print(f"Vector dimensions: {len(vector)}")
print(vector[:10])