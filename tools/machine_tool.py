import pandas as pd


def get_machine_status(machine_id):

    df = pd.read_csv(
        "data/sample_machine_data.csv"
    )

    machine = df[
        df["Machine_ID"] == machine_id
    ]

    if machine.empty:
        return "Machine not found"

    return machine.to_dict(orient="records")[0]