import pandas as pd
from langchain.tools import tool

from utils.data_manager import get_machine_data


@tool
def check_machine_risk(machine_id: str) -> str:
    """
    Check the operational risk of a specific industrial machine
    using the currently uploaded factory data.
    """

    print("\n===== MACHINE RISK TOOL USED =====")

    # Get currently loaded/uploaded CSV
    df = get_machine_data()

    if df is None or df.empty:
        return "No factory machine data is currently loaded."

    # Make sure Machine_ID is treated as text
    df["Machine_ID"] = df["Machine_ID"].astype(str).str.strip()

    machine_id = str(machine_id).strip()

    # Find requested machine
    machine = df[
        df["Machine_ID"].str.upper() == machine_id.upper()
    ]

    if machine.empty:
        return f"Machine {machine_id} was not found in the current factory data."

    row = machine.iloc[0]

    risks = []

    # --------------------------------------------------
    # TEMPERATURE RISK
    # --------------------------------------------------

    temperature = float(row["Temperature"])

    if temperature > 84:
        risks.append(
            f"High temperature ({temperature:.1f} °C)"
        )

    # --------------------------------------------------
    # VIBRATION RISK
    # --------------------------------------------------

    vibration = float(row["Vibration"])

    if vibration > 1.4:
        risks.append(
            f"High vibration ({vibration:.2f})"
        )

    # --------------------------------------------------
    # RUNTIME RISK
    # --------------------------------------------------

    runtime = float(row["Runtime_Hours"])

    if runtime > 1500:
        risks.append(
            f"High runtime ({runtime:.0f} hours)"
        )

    # --------------------------------------------------
    # HEALTH STATUS
    # --------------------------------------------------

    health_status = str(
        row["Health_Status"]
    ).strip()

    # Add health status as a risk indicator
    if health_status.lower() == "critical":
        risks.append(
            "Machine is currently in Critical health status."
        )

    elif health_status.lower() == "warning":
        risks.append(
            "Machine is currently in Warning health status."
        )

    # --------------------------------------------------
    # NO ABNORMALITY
    # --------------------------------------------------

    if not risks:
        risks.append(
            "No major abnormal operating parameter detected."
        )

    # --------------------------------------------------
    # RISK LEVEL
    # --------------------------------------------------

    if health_status.lower() == "critical":
        risk_level = "CRITICAL"

    elif health_status.lower() == "warning":
        risk_level = "WARNING"

    else:
        risk_level = "LOW"

    # --------------------------------------------------
    # RECOMMENDATION
    # --------------------------------------------------

    if risk_level == "CRITICAL":

        recommendation = (
            "Immediate inspection and maintenance are recommended. "
            "The machine may require priority attention."
        )

    elif risk_level == "WARNING":

        recommendation = (
            "Monitor the machine closely and schedule inspection "
            "if abnormal conditions continue."
        )

    else:

        recommendation = (
            "Machine is operating normally. "
            "Continue routine monitoring and maintenance."
        )

    # --------------------------------------------------
    # FINAL REPORT
    # --------------------------------------------------

    return f"""
MACHINE RISK ASSESSMENT

Machine ID: {row["Machine_ID"]}
Machine Type: {row["Machine_Name"]}
Location: {row["Location"]}

Risk Level: {risk_level}
Health Status: {health_status}

Operating Parameters:

Temperature: {temperature:.2f} °C
Vibration: {vibration:.2f}
Runtime: {runtime:.0f} hours

Detected Risks:
- {"\n- ".join(risks)}

Recommendation:
{recommendation}
"""