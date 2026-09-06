import pandas as pd
from langchain.tools import tool

from utils.data_manager import get_machine_data


# ==========================================================
# LOAD CURRENT FACTORY DATA
# ==========================================================

def load_data():

    df = get_machine_data()

    if df is None or df.empty:
        raise ValueError(
            "No factory machine data is currently loaded."
        )

    return df


# ==========================================================
# WARNING MACHINES
# ==========================================================

@tool
def get_warning_machines():
    """
    Get machines that are currently in warning condition
    and need monitoring.
    """

    df = load_data()

    warning = df[
        df["Health_Status"].str.strip().str.lower() == "warning"
    ]

    return warning.to_dict(
        orient="records"
    )


# ==========================================================
# HEALTHY MACHINES
# ==========================================================

@tool
def get_healthy_machines():
    """
    Get machines that are operating normally
    with healthy status.
    """

    df = load_data()

    healthy = df[
        df["Health_Status"].str.strip().str.lower() == "healthy"
    ]

    return healthy.to_dict(
        orient="records"
    )


# ==========================================================
# HEALTH SUMMARY
# ==========================================================

@tool
def get_health_summary():
    """
    Provide overall factory machine health statistics.
    """

    df = load_data()

    status = (
        df["Health_Status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    summary = {
        "Total Machines": len(df),

        "Healthy Machines": int(
            (status == "healthy").sum()
        ),

        "Warning Machines": int(
            (status == "warning").sum()
        ),

        "Critical Machines": int(
            (status == "critical").sum()
        )
    }

    return summary