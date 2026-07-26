from dotenv import load_dotenv
import os
import faiss
import numpy as np

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


# --------------------------------------------------
# 1. Load Gemini Embedding Model
# --------------------------------------------------

print("1. Loading embedding model...")

embeddings_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("Geminie_Api_key")
)


# --------------------------------------------------
# 2. Load FAISS Vector Database
# --------------------------------------------------

print("2. Loading FAISS index...")

index = faiss.read_index(
    "RAG/faiss_index.bin"
)


# --------------------------------------------------
# 3. Load Knowledge Documents
# --------------------------------------------------

print("3. Loading knowledge documents...")

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


print("Total documents:", len(documents))


# --------------------------------------------------
# 4. Ask a Question
# --------------------------------------------------

question = "Why does a CNC machine have high vibration?"

print("\nQuestion:")
print(question)


# --------------------------------------------------
# 5. Convert Question to Vector
# --------------------------------------------------

print("\n4. Creating question embedding...")

question_vector = embeddings_model.embed_query(
    question
)


question_vector = np.array(
    [question_vector],
    dtype="float32"
)


# --------------------------------------------------
# 6. Search FAISS
# --------------------------------------------------

print("5. Searching relevant knowledge...")

distances, indices = index.search(
    question_vector,
    3
)


retrieved_knowledge = []


for index_number in indices[0]:

    retrieved_knowledge.append(
        documents[index_number]
    )


context = "\n\n".join(
    retrieved_knowledge
)


print("\nRelevant knowledge retrieved successfully!")


# --------------------------------------------------
# 7. Load Gemini AI Model
# --------------------------------------------------

print("6. Loading Gemini AI model...")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    google_api_key=os.getenv("Geminie_Api_key"),
    temperature=0.2
)


# --------------------------------------------------
# 8. Create RAG Prompt
# --------------------------------------------------

prompt = f"""
You are an AI Industrial Operations Advisor.

Answer the user's question using the industrial maintenance knowledge provided below.

IMPORTANT RULES:
- Use the provided knowledge as the primary source.
- Do not invent technical facts that are not supported by the knowledge.
- Give a clear and well-organized answer.
- Use headings and bullet points where useful.
- Provide practical maintenance recommendations.
- Mention safety considerations when relevant.

INDUSTRIAL MAINTENANCE KNOWLEDGE:
{context}

USER QUESTION:
{question}

Now provide the final answer.
"""


# --------------------------------------------------
# 9. Generate Final Answer
# --------------------------------------------------

print("7. Generating final answer...")

response = llm.invoke(
    prompt
)


print("\n" + "=" * 60)
print("FINAL RAG ANSWER")
print("=" * 60)

print(response.content)



