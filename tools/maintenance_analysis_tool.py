import pandas as pd
from langchain.tools import tool


CSV_PATH = "data/sample_machine_data.csv"


@tool
def analyze_maintenance_issues():
    """
    Analyze machine data and identify the most common
    operational issues requiring maintenance attention.
    """

    df = pd.read_csv(CSV_PATH)

    # Define operational conditions

    high_vibration = df[
        df["Vibration"] > 1.4
    ]

    high_temperature = df[
        df["Temperature"] > 84
    ]

    high_runtime = df[
        df["Runtime_Hours"] > 1500
    ]

    critical_machines = df[
        df["Health_Status"] == "Critical"
    ]

    warning_machines = df[
        df["Health_Status"] == "Warning"
    ]

    # Count issues

    issue_counts = {
        "High Vibration": len(high_vibration),
        "High Temperature": len(high_temperature),
        "High Runtime": len(high_runtime)
    }

    # Find most common issue

    most_common_issue = max(
        issue_counts,
        key=issue_counts.get
    )

    most_common_count = issue_counts[
        most_common_issue
    ]

    # Create report

    report = f"""
MAINTENANCE ISSUE ANALYSIS

Total Machines Analyzed: {len(df)}

Issue Frequency:

High Vibration: {issue_counts["High Vibration"]}
High Temperature: {issue_counts["High Temperature"]}
High Runtime: {issue_counts["High Runtime"]}


Most Common Issue:
{most_common_issue} ({most_common_count} machines)

Recommendation:
Prioritize maintenance investigation for the most
frequent operational issue and monitor affected machines.
"""

    return report