import sqlite3
from langchain.tools import tool


DB_PATH = "data/maintenance.db"


@tool
def analyze_maintenance_by_location():
    """
    Analyze maintenance workload across factory locations.
    """

    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            location,
            COUNT(*) AS maintenance_tasks,
            SUM(
                CASE
                    WHEN maintenance_status = 'Pending'
                    THEN 1
                    ELSE 0
                END
            ) AS pending_tasks,
            SUM(
                CASE
                    WHEN maintenance_status = 'Completed'
                    THEN 1
                    ELSE 0
                END
            ) AS completed_tasks
        FROM maintenance
        GROUP BY location
        ORDER BY maintenance_tasks DESC
    """

    rows = conn.execute(query).fetchall()

    conn.close()

    if not rows:
        return "No maintenance records found."

    most_active_location = rows[0][0]
    highest_task_count = rows[0][1]

    report = """
MAINTENANCE LOCATION ANALYSIS

Maintenance workload by location:

"""

    for location, total, pending, completed in rows:

        report += (
            f"{location}: "
            f"{total} total tasks, "
            f"{pending} pending, "
            f"{completed} completed\n"
        )

    report += (
        f"\nHighest Maintenance Workload:\n"
        f"{most_active_location} "
        f"({highest_task_count} tasks)\n\n"
        "Recommendation:\n"
        "Prioritize maintenance resources and technician "
        "availability in the location with the highest workload."
    )

    return report