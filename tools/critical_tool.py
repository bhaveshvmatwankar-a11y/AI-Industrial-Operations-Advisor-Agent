from langchain.tools import tool


@tool
def get_critical_machines():
    """
    Fetches critical machines from industrial sensor CSV data.
    """

    import pandas as pd

    df = pd.read_csv(
        "data/sample_machine_data.csv"
    )

    df.columns = df.columns.str.strip()

    critical = df[
        df["Health_Status"] == "Critical"
        ]

    return critical.to_dict(
        orient="records"
    )