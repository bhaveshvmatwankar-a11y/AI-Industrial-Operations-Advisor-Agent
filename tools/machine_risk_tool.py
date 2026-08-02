import pandas as pd
from langchain.tools import tool


@tool
def check_machine_risk(machine_id: str) -> str:
    """
    Check the operational risk of a specific industrial machine
    using temperature, vibration, pressure, current and health status.
    """

    print("\n===== MACHINE RISK TOOL USED =====")

    df = pd.read_csv("data/sample_machine_data.csv")

    machine = df[
        df["Machine_ID"].str.upper() == machine_id.upper()
    ]

    if machine.empty:
        return f"Machine {machine_id} was not found."

    row = machine.iloc[0]

    risks = []

    if row["Temperature"] > 84:
        risks.append(
            f"High temperature ({row['Temperature']:.1f} °C)"
        )

    if row["Vibration"] > 1.4:
        risks.append(
            f"High vibration ({row['Vibration']:.2f})"
        )

    if row["Pressure"] > 3.5:
        risks.append(
            f"High pressure ({row['Pressure']:.2f})"
        )

    if row["Current"] > 25:
        risks.append(
            f"High current ({row['Current']:.2f} A)"
        )

    if not risks:
        risks.append("No major abnormal operating parameter detected.")

    risk_level = row["Health_Status"]

    return f"""
MACHINE RISK ASSESSMENT

Machine ID: {row["Machine_ID"]}
Machine Type: {row["Machine_Name"]}
Location: {row["Location"]}

Health Status: {risk_level}

Temperature: {row["Temperature"]:.2f} °C
Pressure: {row["Pressure"]:.2f}
Vibration: {row["Vibration"]:.2f}
Current: {row["Current"]:.2f} A
Runtime: {row["Runtime_Hours"]} hours

Detected Risks:
- {"\n- ".join(risks)}

Recommendation:
Follow appropriate industrial safety procedures and
have qualified maintenance personnel inspect the machine
if abnormal conditions persist.
"""