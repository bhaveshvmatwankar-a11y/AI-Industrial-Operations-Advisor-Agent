from dotenv import load_dotenv

import os

print("USING THIS AGENT FILE:", __file__)

from RAG.rag_retriever import retrieve_knowledge

from langchain_google_genai import ChatGoogleGenerativeAI

from tools.critical_tool import get_critical_machines

from tools.health_tool import (
    get_warning_machines,
    get_healthy_machines,
    get_health_summary
)

from langchain.agents import create_agent


load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    google_api_key=os.getenv("Geminie_Api_key"),
    temperature=0,


)

print("MODEL LOADED: gemini-3.1-flash-lite")


tools = [
    get_critical_machines,
    get_warning_machines,
    get_healthy_machines,
    get_health_summary,
    retrieve_knowledge
]


system_prompt = """
You are an Industrial Operations Advisor AI.

You assist factory managers with machine monitoring,
predictive maintenance and operational decisions.

Rules:

- Use simple human understandable language.
- Avoid unnecessary technical jargon.
- Format answers like an industrial dashboard.
- Give short summaries.
- Mention risks and recommendations.

- For questions about industrial machines, maintenance problems,
  abnormal conditions, vibration, temperature, pressure, failure causes,
  or maintenance recommendations, use the retrieve_knowledge tool first.

For health reports:

## Machine Health Summary

Healthy:
Explain normal machines.

Warning:
Explain machines requiring monitoring.

Critical:
Explain machines requiring immediate action.

Recommendation:
Give maintenance advice.

Keep responses concise and professional.
"""


agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)