import sqlite3
from langchain.tools import tool

from tools.maintenance_tracker import get_active_db_path


@tool
def get_maintenance_machine_summary() -> str:
    """
    Summarize unique machines present in the maintenance database.
    Distinguishes maintenance records/tasks from unique machines.
    """

    db_path = get_active_db_path()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Total maintenance records/tasks
    cursor.execute("""
        SELECT COUNT(*)
        FROM maintenance
    """)
    total_tasks = cursor.fetchone()[0]

    # Unique machines
    cursor.execute("""
        SELECT COUNT(DISTINCT machine_id)
        FROM maintenance
    """)
    unique_machines = cursor.fetchone()[0]

    # Unique machines with pending maintenance
    cursor.execute("""
        SELECT COUNT(DISTINCT machine_id)
        FROM maintenance
        WHERE LOWER(TRIM(maintenance_status)) = 'pending'
    """)
    pending_machines = cursor.fetchone()[0]

    # Unique machines currently in progress
    cursor.execute("""
        SELECT COUNT(DISTINCT machine_id)
        FROM maintenance
        WHERE LOWER(TRIM(maintenance_status)) = 'in progress'
    """)
    in_progress_machines = cursor.fetchone()[0]

    # Unique machines with completed maintenance
    cursor.execute("""
        SELECT COUNT(DISTINCT machine_id)
        FROM maintenance
        WHERE LOWER(TRIM(maintenance_status)) = 'completed'
    """)
    completed_machines = cursor.fetchone()[0]

    conn.close()

    return f"""
MAINTENANCE MACHINE SUMMARY

Unique Machines in Maintenance Database:
{unique_machines}

Total Maintenance Tasks/Records:
{total_tasks}

Machines with Pending Maintenance:
{pending_machines}

Machines Currently In Progress:
{in_progress_machines}

Machines with Completed Maintenance:
{completed_machines}

Important:
A maintenance task/record is not necessarily a unique machine.
The unique machine count is calculated using DISTINCT Machine IDs.
"""


@tool
def get_pending_maintenance_machines() -> str:
    """
    Return all unique machines that currently have pending maintenance.
    Used when the user asks which machines have pending maintenance.
    """

    db_path = get_active_db_path()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # First inspect the available columns dynamically.
    cursor.execute("PRAGMA table_info(maintenance)")
    columns = [row[1] for row in cursor.fetchall()]

    # Basic query using columns that we know exist.
    cursor.execute("""
        SELECT DISTINCT machine_id
        FROM maintenance
        WHERE LOWER(TRIM(maintenance_status)) = 'pending'
        ORDER BY machine_id
    """)

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return "No machines currently have pending maintenance."

    result = f"""
PENDING MAINTENANCE MACHINES

Total Unique Machines with Pending Maintenance:
{len(rows)}

Machine IDs:
"""

    for row in rows:
        result += f"- {row[0]}\n"

    return result