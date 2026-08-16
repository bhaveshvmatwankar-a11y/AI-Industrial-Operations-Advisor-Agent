import sqlite3
from datetime import date
import pandas as pd
from datetime import date

DB_PATH = "data/maintenance.db"


def initialize_database():
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS maintenance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id TEXT NOT NULL,
            maintenance_status TEXT NOT NULL,
            maintenance_date TEXT,
            notes TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_maintenance(
    machine_id,
    status="Pending",
    maintenance_date=None,
    notes=""
):
    initialize_database()

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    if maintenance_date is None:
        maintenance_date = str(date.today())

    cursor.execute("""
        INSERT INTO maintenance
        (
            machine_id,
            maintenance_status,
            maintenance_date,
            notes
        )
        VALUES (?, ?, ?, ?)
    """, (
        machine_id,
        status,
        maintenance_date,
        notes
    ))

    conn.commit()
    conn.close()


def get_maintenance_records():
    initialize_database()

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            machine_id,
            maintenance_status,
            maintenance_date,
            notes
        FROM maintenance
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records


def get_maintenance_progress():

    initialize_database()

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM maintenance
    """)

    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM maintenance
        WHERE maintenance_status = 'Completed'
    """)

    completed = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM maintenance
        WHERE maintenance_status = 'In Progress'
    """)

    in_progress = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM maintenance
        WHERE maintenance_status = 'Pending'
    """)

    pending = cursor.fetchone()[0]

    conn.close()

    if total > 0:
        progress = (completed / total) * 100
    else:
        progress = 0

    return {
        "Total": total,
        "Completed": completed,
        "In Progress": in_progress,
        "Pending": pending,
        "Progress_Percentage": round(progress, 2)
    }

from langchain.tools import tool


@tool
def get_maintenance_progress_report() -> str:
    """
    Get the current industrial maintenance progress
    from the SQLite maintenance database.
    """

    progress = get_maintenance_progress()

    return f"""
MAINTENANCE PROGRESS REPORT

Total Maintenance Tasks: {progress["Total"]}

Completed: {progress["Completed"]}
In Progress: {progress["In Progress"]}
Pending: {progress["Pending"]}

Overall Progress: {progress["Progress_Percentage"]}%

Maintenance Status:
- Completed tasks have been finished.
- In-progress tasks are currently being handled.
- Pending tasks still require maintenance attention.
"""


@tool
def get_pending_critical_maintenance() -> str:
    """
    Find critical machines from the machine dataset
    that currently have pending maintenance.
    """

    machine_df = pd.read_csv(
        "data/sample_machine_data.csv"
    )

    conn = sqlite3.connect(
        DB_PATH
    )

    maintenance_df = pd.read_sql_query(
        """
        SELECT *
        FROM maintenance
        WHERE maintenance_status = 'Pending'
        """,
        conn
    )

    conn.close()

    critical_machines = machine_df[
        machine_df["Health_Status"] == "Critical"
    ]

    result = critical_machines.merge(
        maintenance_df,
        left_on="Machine_ID",
        right_on="machine_id",
        how="inner"
    )

    if result.empty:
        return "No critical machines currently have pending maintenance."

    return result[
        [
            "Machine_ID",
            "Machine_Name",
            "Location",
            "Temperature",
            "Vibration",
            "Runtime_Hours",
            "maintenance_status",
            "maintenance_type",
            "notes"
        ]
    ].to_string(index=False)