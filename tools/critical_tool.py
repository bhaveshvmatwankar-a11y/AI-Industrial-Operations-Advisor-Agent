from langchain.tools import tool

from utils.data_manager import get_machine_data


@tool
def get_critical_machines():
    """
    Fetch machines that are currently in critical condition
    from the active factory dataset.
    """

    df = get_machine_data()

    if df is None or df.empty:
        return "No factory machine data is currently loaded."

    df = df.copy()

    df.columns = df.columns.str.strip()

    critical = df[
        df["Health_Status"]
        .astype(str)
        .str.strip()
        .str.lower()
        == "critical"
    ]

    return critical.to_dict(
        orient="records"
    )