import sqlite3
import pandas as pd
from langchain.tools import tool


CSV_PATH = "data/sample_machine_data.csv"
DB_PATH = "data/maintenance.db"


@tool
def analyze_maintenance_coverage():
    """
    Analyze maintenance coverage for machines that are
    currently included in the maintenance schedule.
    """

    # Load machine data
    machine_df = pd.read_csv(CSV_PATH)

    # Load maintenance schedule
    conn = sqlite3.connect(DB_PATH)

    maintenance_df = pd.read_sql_query(
        "SELECT * FROM maintenance",
        conn
    )

    conn.close()

    # Find machines in the maintenance schedule
    scheduled_machine_ids = (
        maintenance_df["machine_id"]
        .unique()
    )

    scheduled_df = machine_df[
        machine_df["Machine_ID"].isin(
            scheduled_machine_ids
        )
    ].copy()

    # Critical machines within maintenance schedule
    critical_scheduled = scheduled_df[
        scheduled_df["Health_Status"] == "Critical"
    ]

    total_scheduled = len(scheduled_df)
    total_critical = len(critical_scheduled)

    # Join scheduled machines with maintenance status
    result = critical_scheduled.merge(
        maintenance_df,
        left_on="Machine_ID",
        right_on="machine_id",
        how="left"
    )

    completed = len(
        result[
            result["maintenance_status"] == "Completed"
        ]
    )

    in_progress = len(
        result[
            result["maintenance_status"] == "In Progress"
        ]
    )

    pending = len(
        result[
            result["maintenance_status"] == "Pending"
        ]
    )

    # Maintenance attention among scheduled critical machines
    attention = completed + in_progress

    attention_percentage = (
        attention / total_critical * 100
        if total_critical > 0
        else 0
    )

    report = f"""
CRITICAL MAINTENANCE COVERAGE ANALYSIS

Total Factory Machines: {len(machine_df)}

Machines in Maintenance Schedule: {total_scheduled}

Critical Machines in Maintenance Schedule: {total_critical}

Maintenance Status of Scheduled Critical Machines:

Completed: {completed}
In Progress: {in_progress}
Pending: {pending}

Active Maintenance Attention:
{attention_percentage:.1f}%

Critical Machines Requiring Attention:
"""

    if pending > 0:

        pending_machines = result[
            result["maintenance_status"] == "Pending"
        ]

        for _, row in pending_machines.iterrows():

            report += (
                f"\n- {row['Machine_ID']} | "
                f"{row['Machine_Name']} | "
                f"{row['Location']} | "
                f"Vibration: {row['Vibration']:.2f}"
            )

    else:

        report += "\nNo scheduled critical machines have pending maintenance."

    if pending > 0:

        report += f"""

Recommendation:

{pending} scheduled critical machine(s) have pending
maintenance. These machines should be prioritized
for immediate maintenance attention.
"""

    else:

        report += """

Recommendation:

No scheduled critical machines currently have pending
maintenance. Continue monitoring their condition and
follow the maintenance schedule.
"""

    return report