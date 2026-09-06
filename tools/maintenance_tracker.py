import sqlite3
from datetime import date

import pandas as pd
from langchain.tools import tool

from utils.data_manager import get_machine_data


# =========================================================
# ACTIVE DATABASE
# =========================================================

# =========================================================
# ACTIVE MAINTENANCE DATABASE
# =========================================================

ACTIVE_DB_PATH = None


def set_active_db_path(db_path):
    global ACTIVE_DB_PATH

    if db_path and str(db_path).strip():
        ACTIVE_DB_PATH = str(db_path).strip()


def get_active_db_path():

    global ACTIVE_DB_PATH

    # First use application-level active DB
    if ACTIVE_DB_PATH:
        return ACTIVE_DB_PATH

    # Then try Streamlit session state
    try:
        import streamlit as st

        db_path = st.session_state.get(
            "maintenance_db_path"
        )

        if db_path:
            ACTIVE_DB_PATH = db_path
            return db_path

    except Exception:
        pass

    raise RuntimeError(
        "No maintenance database is currently active."
    )


def get_active_db_info():

    return {
        "path": get_active_db_path()
    }


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

def initialize_database():

    db_path = get_active_db_path()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS maintenance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id TEXT NOT NULL,
            machine_name TEXT,
            location TEXT,
            health_status TEXT,
            maintenance_status TEXT NOT NULL,
            maintenance_date TEXT,
            maintenance_type TEXT,
            notes TEXT
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# ADD MAINTENANCE
# =========================================================

def add_maintenance(
    machine_id,
    status="Pending",
    maintenance_date=None,
    notes=""
):

    initialize_database()

    db_path = get_active_db_path()

    conn = sqlite3.connect(db_path)
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


# =========================================================
# GET MAINTENANCE RECORDS
# =========================================================

def get_maintenance_records():

    initialize_database()

    db_path = get_active_db_path()

    conn = sqlite3.connect(db_path)
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


# =========================================================
# MAINTENANCE PROGRESS
# =========================================================

def get_maintenance_progress():

    initialize_database()

    db_path = get_active_db_path()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Total
    cursor.execute("""
        SELECT COUNT(*)
        FROM maintenance
    """)

    total = cursor.fetchone()[0]

    # Completed
    cursor.execute("""
        SELECT COUNT(*)
        FROM maintenance
        WHERE LOWER(TRIM(maintenance_status)) = 'completed'
    """)

    completed = cursor.fetchone()[0]

    # In Progress
    cursor.execute("""
        SELECT COUNT(*)
        FROM maintenance
        WHERE LOWER(TRIM(maintenance_status)) = 'in progress'
    """)

    in_progress = cursor.fetchone()[0]

    # Pending
    cursor.execute("""
        SELECT COUNT(*)
        FROM maintenance
        WHERE LOWER(TRIM(maintenance_status)) = 'pending'
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


# =========================================================
# TOOL 1: DATABASE SUMMARY
# =========================================================

@tool
def get_maintenance_database_summary() -> str:
    """
    Return the number of maintenance records and unique machines
    in the currently active maintenance database.
    """

    try:

        db_path = get_active_db_path()

        conn = sqlite3.connect(db_path)

        # Overall summary
        summary = pd.read_sql_query(
            """
            SELECT
                COUNT(*) AS total_records,
                COUNT(DISTINCT machine_id) AS unique_machines
            FROM maintenance
            """,
            conn
        )

        # Status summary
        status_df = pd.read_sql_query(
            """
            SELECT
                LOWER(TRIM(maintenance_status)) AS status,
                COUNT(*) AS count
            FROM maintenance
            GROUP BY LOWER(TRIM(maintenance_status))
            """,
            conn
        )

        conn.close()

        total_records = int(
            summary.iloc[0]["total_records"]
        )

        unique_machines = int(
            summary.iloc[0]["unique_machines"]
        )

        output = f"""
MAINTENANCE DATABASE SUMMARY

Active Database:
{db_path}

Total Maintenance Records: {total_records}

Unique Machines in Maintenance Database: {unique_machines}

Maintenance Status:
"""

        for _, row in status_df.iterrows():

            output += (
                f"- {row['status'].title()}: "
                f"{int(row['count'])}\n"
            )

        return output

    except Exception as e:

        return (
            f"Unable to read maintenance database: {e}"
        )


# =========================================================
# TOOL 2: MAINTENANCE PROGRESS
# =========================================================

@tool
def get_maintenance_progress_report() -> str:
    """
    Get the current industrial maintenance progress
    from the active SQLite maintenance database.
    """

    try:

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

    except Exception as e:

        return (
            f"Unable to read maintenance progress: {e}"
        )


# =========================================================
# TOOL 3: PENDING CRITICAL MAINTENANCE
# =========================================================

@tool
def get_pending_critical_maintenance() -> str:
    """
    Find critical machines from the currently loaded machine dataset
    that have pending maintenance in the active maintenance database.
    """

    try:

        machine_df = get_machine_data()

        if machine_df is None or machine_df.empty:
            return "No machine data is currently loaded."

        initialize_database()

        db_path = get_active_db_path()

        conn = sqlite3.connect(db_path)

        maintenance_df = pd.read_sql_query(
            """
            SELECT *
            FROM maintenance
            WHERE LOWER(TRIM(maintenance_status)) = 'pending'
            """,
            conn
        )

        conn.close()

        if maintenance_df.empty:
            return "No machines currently have pending maintenance."

        # Find critical machines
        critical_machines = machine_df[
            machine_df["Health_Status"]
            .astype(str)
            .str.strip()
            .str.lower() == "critical"
        ]

        if critical_machines.empty:
            return (
                "No critical machines are currently "
                "present in the machine dataset."
            )

        # Match critical machines with pending maintenance
        result = critical_machines.merge(
            maintenance_df,
            left_on="Machine_ID",
            right_on="machine_id",
            how="inner"
        )

        if result.empty:

            return (
                "No critical machines currently have "
                "pending maintenance in the maintenance database."
            )

        output = (
            "CRITICAL MACHINES WITH "
            "PENDING MAINTENANCE\n\n"
        )

        for _, row in result.iterrows():

            output += f"""
Machine ID: {row["Machine_ID"]}

Machine Name: {row["Machine_Name"]}

Location: {row["Location"]}

Health Status: {row["Health_Status"]}

Temperature: {row["Temperature"]:.2f} °C

Vibration: {row["Vibration"]:.2f}

Runtime: {row["Runtime_Hours"]} hours

Maintenance Status: {row["maintenance_status"]}

Maintenance Type: {row.get("maintenance_type", "Not specified")}

Notes: {row.get("notes", "No notes")}

"""

        output += """
Recommendation:

Prioritize these critical machines for immediate
maintenance attention.
"""

        return output

    except Exception as e:

        return (
            f"Unable to analyze critical maintenance: {e}"
        )