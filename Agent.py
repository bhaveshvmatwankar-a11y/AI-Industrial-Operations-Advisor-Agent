from dotenv import load_dotenv

import os

print("USING THIS AGENT FILE:", __file__)

from RAG.rag_retriever import retrieve_knowledge

from langchain_google_genai import ChatGoogleGenerativeAI

from tools.critical_tool import get_critical_machines

from tools.machine_risk_tool import check_machine_risk

from tools.maintenance_priority_tool import get_maintenance_priorities

from tools.maintenance_coverage_analysis import (
    analyze_maintenance_coverage
)

from tools.factory_operational_insight import (
    generate_factory_operational_insight
)

from tools.maintenance_tracker import get_maintenance_progress_report

from tools.maintenance_analysis_tool import analyze_maintenance_issues

from tools.health_tool import (
    get_warning_machines,
    get_healthy_machines,
    get_health_summary
)

from tools.maintenance_tracker import (
    get_maintenance_progress_report,
    get_pending_critical_maintenance
)

from tools.maintenance_location_analysis import (
    analyze_maintenance_by_location
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
    retrieve_knowledge,
    check_machine_risk,
    get_maintenance_priorities,
    get_maintenance_progress_report,
    get_pending_critical_maintenance,
    analyze_maintenance_issues,
    analyze_maintenance_by_location,
    analyze_maintenance_coverage,
    generate_factory_operational_insight

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

TOOL SELECTION:

- For questions about a specific machine ID such as M001,
  use the check_machine_risk tool.

- For questions asking which machines are critical,
  use the get_critical_machines tool.

- For questions asking about warning or healthy machines,
  use the appropriate health tools.

- For questions asking which machines require maintenance,
  which machines should be prioritized,
  maintenance urgency, or maintenance scheduling,
  use the get_maintenance_priorities tool.

- For questions about industrial maintenance knowledge,
  failure causes, abnormal conditions, vibration causes,
  temperature causes, pressure problems, or general
  maintenance recommendations, use the retrieve_knowledge tool.

- If a question requires both actual machine data and
  industrial maintenance knowledge, use both the appropriate
  machine tool and retrieve_knowledge.

- Combine information from multiple tools when necessary
  and provide one clear final recommendation.
  
- For questions about maintenance progress,
  completed maintenance, pending maintenance,
  maintenance tasks, or maintenance completion percentage,
  use the get_maintenance_progress_report tool.
  
- For questions asking about critical machines
  with pending maintenance, use the
  get_pending_critical_maintenance tool.
  
- For questions asking about the most common operational
  problems, issue frequency, high vibration, high temperature,
  or high runtime across machines, use the
  analyze_maintenance_issues tool.
  
- For questions about maintenance workload by factory
  location, maintenance concentration, or which location
  has the highest maintenance workload, use the
  analyze_maintenance_by_location tool.
  
- For questions about critical machines within the
  maintenance schedule and their maintenance coverage,
  use the analyze_maintenance_coverage tool.
  
- For questions asking for an overall factory operational
  insight report, combined machine and maintenance analysis,
  major operational issues, or management-level recommendations,
  use the generate_factory_operational_insight tool.

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