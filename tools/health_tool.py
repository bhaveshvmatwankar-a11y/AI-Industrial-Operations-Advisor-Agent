import pandas as pd
from langchain.tools import tool


CSV_PATH = "data/sample_machine_data.csv"


def load_data():
    return pd.read_csv(CSV_PATH)


@tool
def get_warning_machines():
    """
    Get machines that are currently in warning condition and need monitoring.
    """

    df = load_data()

    warning = df[df["Health_Status"] == "Warning"]

    return warning.to_dict(orient="records")


@tool
def get_healthy_machines():
    """
    Get machines that are operating normally with healthy status.
    """

    df = load_data()

    healthy = df[df["Health_Status"] == "Healthy"]

    return healthy.to_dict(orient="records")


@tool
def get_health_summary():
    """
    Provide overall factory machine health statistics.
    """

    df = load_data()

    summary = {
        "Total Machines": len(df),
        "Healthy Machines": len(df[df["Health_Status"] == "Healthy"]),
        "Warning Machines": len(df[df["Health_Status"] == "Warning"]),
        "Critical Machines": len(df[df["Health_Status"] == "Critical"])
    }

    return summary