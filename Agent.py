from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI

# Load variables from .env
load_dotenv()

# Create Gemini model
llm = ChatGoogleGenerativeAI(
    model="models/gemini-3.5-flash",
    google_api_key=os.getenv("Geminie_Api_key")
)


system_prompt = """
You are an Industrial Operations Advisor AI.

Your job is to help factory managers monitor machines,
predict failures, and improve maintenance decisions.

give the answers in point wise with numbering at start

Give concise answers in 3-4 sentences.
make easy to understand
Use industrial terminology.
"""

# Send a test prompt
response = llm.invoke(
    system_prompt+"\n explain the predictive maintanence.!"
)

# Print the AI response
print(response.content[0]["text"])