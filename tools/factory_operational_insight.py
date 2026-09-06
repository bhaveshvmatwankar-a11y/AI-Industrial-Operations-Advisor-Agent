from langchain.tools import tool

from utils.data_manager import get_machine_data
from tools.company_context_tool import get_company_name


@tool
def generate_factory_operational_insight():
    """
    Generate a factory-level operational insight report
    using the currently loaded machine data.
    """

    # ======================================================
    # COMPANY NAME
    # ======================================================

    company_name = get_company_name()

    # ======================================================
    # MACHINE DATA
    # ======================================================

    df = get_machine_data()

    if df is None or df.empty:
        return "No factory machine data is currently loaded."

    # ======================================================
    # MACHINE ANALYSIS
    # ======================================================

    high_vibration = len(
        df[df["Vibration"] > 1.4]
    )

    high_temperature = len(
        df[df["Temperature"] > 84]
    )

    high_runtime = len(
        df[df["Runtime_Hours"] > 1500]
    )

    issue_counts = {
        "High Vibration": high_vibration,
        "High Temperature": high_temperature,
        "High Runtime": high_runtime
    }

    most_common_issue = max(
        issue_counts,
        key=issue_counts.get
    )

    # ======================================================
    # REPORT
    # ======================================================

    report = f"""
FACTORY OPERATIONAL INSIGHT REPORT

Company: {company_name}

Machine Health Overview:

Total Machines: {len(df)}

High Vibration: {high_vibration}
High Temperature: {high_temperature}
High Runtime: {high_runtime}

Most Common Operational Issue:
{most_common_issue}

Key Findings:

- {most_common_issue} is the most frequent
  operational issue in the current machine dataset.

Recommendations:

1. Prioritize investigation of
   {most_common_issue.lower()} conditions.

2. Continue monitoring machines showing
   abnormal operating parameters.

3. Ensure maintenance records are kept
   up-to-date for accurate maintenance analysis.
"""

    return report