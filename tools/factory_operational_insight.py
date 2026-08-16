import pandas as pd
import sqlite3
from langchain.tools import tool


CSV_PATH = "data/sample_machine_data.csv"
DB_PATH = "data/maintenance.db"


@tool
def generate_factory_operational_insight():
    """
    Generate a factory-level operational insight report
    using machine conditions and maintenance data.
    """

    # -------------------------------
    # MACHINE DATA ANALYSIS
    # -------------------------------

    df = pd.read_csv(CSV_PATH)

    high_vibration = len(
        df[df["Vibration"] > 1.4]
    )

    high_temperature = len(
        df[df["Temperature"] > 84]
    )

    high_runtime = len(
        df[df["Runtime_Hours"] > 1500]
    )

    most_common_issue = max(
        {
            "High Vibration": high_vibration,
            "High Temperature": high_temperature,
            "High Runtime": high_runtime
        },
        key={
            "High Vibration": high_vibration,
            "High Temperature": high_temperature,
            "High Runtime": high_runtime
        }.get
    )

    # -------------------------------
    # MAINTENANCE DATA
    # -------------------------------

    conn = sqlite3.connect(DB_PATH)

    maintenance_df = pd.read_sql_query(
        "SELECT * FROM maintenance",
        conn
    )

    conn.close()

    # Location workload
    location_counts = (
        maintenance_df["location"]
        .value_counts()
    )

    highest_location = location_counts.index[0]
    highest_location_tasks = location_counts.iloc[0]

    # Critical machines within schedule
    scheduled_ids = maintenance_df[
        "machine_id"
    ].unique()

    scheduled_df = df[
        df["Machine_ID"].isin(scheduled_ids)
    ]

    critical_scheduled = scheduled_df[
        scheduled_df["Health_Status"] == "Critical"
    ]

    critical_ids = critical_scheduled[
        "Machine_ID"
    ].tolist()

    critical_maintenance = maintenance_df[
        maintenance_df["machine_id"].isin(
            critical_ids
        )
    ]

    critical_pending = len(
        critical_maintenance[
            critical_maintenance[
                "maintenance_status"
            ] == "Pending"
        ]
    )

    critical_in_progress = len(
        critical_maintenance[
            critical_maintenance[
                "maintenance_status"
            ] == "In Progress"
        ]
    )

    critical_completed = len(
        critical_maintenance[
            critical_maintenance[
                "maintenance_status"
            ] == "Completed"
        ]
    )

    total_critical = len(critical_scheduled)

    # -------------------------------
    # REPORT
    # -------------------------------

    report = f"""
FACTORY OPERATIONAL INSIGHT REPORT

Machine Analysis:

Total Machines: {len(df)}

High Vibration: {high_vibration}
High Temperature: {high_temperature}
High Runtime: {high_runtime}

Most Common Operational Issue:
{most_common_issue}

Maintenance Analysis:

Total Maintenance Tasks:
{len(maintenance_df)}

Highest Maintenance Workload:
{highest_location} ({highest_location_tasks} tasks)

Critical Machines in Maintenance Schedule:
{total_critical}

Critical Maintenance Status:

Completed: {critical_completed}
In Progress: {critical_in_progress}
Pending: {critical_pending}

Operational Insights:
"""

    # -------------------------------
    # INSIGHTS
    # -------------------------------

    report += (
        f"\n- {most_common_issue} is the most frequent "
        f"operational issue in the current machine dataset."
    )

    report += (
        f"\n- {highest_location} has the highest "
        f"maintenance workload with "
        f"{highest_location_tasks} tasks."
    )

    if critical_pending > 0:

        report += (
            f"\n- {critical_pending} critical scheduled "
            f"machine(s) currently have pending maintenance."
        )

    else:

        report += (
            "\n- No critical scheduled machines currently "
            "have pending maintenance."
        )

    # -------------------------------
    # RECOMMENDATIONS
    # -------------------------------

    report += "\n\nRecommendations:\n"

    report += (
        f"1. Prioritize investigation of "
        f"{most_common_issue.lower()} conditions."
    )

    report += (
        f"\n2. Review maintenance workload at "
        f"{highest_location}."
    )

    if critical_pending > 0:

        report += (
            "\n3. Prioritize pending maintenance for "
            "critical machines immediately."
        )

    else:

        report += (
            "\n3. Continue monitoring critical machines "
            "according to the maintenance schedule."
        )

    return report
