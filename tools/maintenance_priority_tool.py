import pandas as pd
from langchain.tools import tool

from utils.data_manager import get_machine_data


@tool
def get_maintenance_priorities() -> str:
    """
    Identify machines that should receive maintenance attention
    based on health status, temperature, vibration, runtime,
    and time since last maintenance.
    """

    # ------------------------------------------------------
    # LOAD ACTIVE FACTORY DATA
    # ------------------------------------------------------

    df = get_machine_data()

    if df is None or df.empty:
        return "No factory machine data is currently loaded."

    df = df.copy()


    # ------------------------------------------------------
    # CHECK REQUIRED COLUMNS
    # ------------------------------------------------------

    required_columns = [
        "Machine_ID",
        "Machine_Name",
        "Location",
        "Health_Status"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        return (
            "Maintenance priority analysis cannot be performed "
            "because the following required columns are missing: "
            + ", ".join(missing_columns)
        )


    # ------------------------------------------------------
    # OPTIONAL COLUMNS
    # ------------------------------------------------------

    if "Temperature" not in df.columns:
        df["Temperature"] = None

    if "Vibration" not in df.columns:
        df["Vibration"] = None

    if "Runtime_Hours" not in df.columns:
        df["Runtime_Hours"] = None

    if "Last_Maintenance" not in df.columns:
        df["Last_Maintenance"] = None


    # ------------------------------------------------------
    # MAINTENANCE DATE
    # ------------------------------------------------------

    df["Last_Maintenance"] = pd.to_datetime(
        df["Last_Maintenance"],
        errors="coerce"
    )

    today = pd.Timestamp.today()

    df["Days_Since_Maintenance"] = (
        today - df["Last_Maintenance"]
    ).dt.days


    # ------------------------------------------------------
    # PRIORITY CALCULATION
    # ------------------------------------------------------

    priorities = []


    for _, row in df.iterrows():

        score = 0
        reasons = []


        # --------------------------------------------------
        # HEALTH STATUS
        # --------------------------------------------------

        health_status = str(
            row["Health_Status"]
        ).strip().lower()


        if health_status == "critical":

            score += 5

            reasons.append(
                "Critical health status"
            )

        elif health_status == "warning":

            score += 3

            reasons.append(
                "Warning health status"
            )


        # --------------------------------------------------
        # TEMPERATURE
        # --------------------------------------------------

        temperature = row["Temperature"]

        if pd.notna(temperature):

            if temperature > 86:

                score += 3

                reasons.append(
                    "High temperature"
                )

            elif temperature > 84:

                score += 1

                reasons.append(
                    "Elevated temperature"
                )


        # --------------------------------------------------
        # VIBRATION
        # --------------------------------------------------

        vibration = row["Vibration"]

        if pd.notna(vibration):

            if vibration > 1.6:

                score += 3

                reasons.append(
                    "High vibration"
                )

            elif vibration > 1.4:

                score += 1

                reasons.append(
                    "Elevated vibration"
                )


        # --------------------------------------------------
        # RUNTIME
        # --------------------------------------------------

        runtime = row["Runtime_Hours"]

        if pd.notna(runtime):

            if runtime > 1800:

                score += 2

                reasons.append(
                    "High runtime"
                )

            elif runtime > 1500:

                score += 1

                reasons.append(
                    "High operating hours"
                )


        # --------------------------------------------------
        # MAINTENANCE AGE
        # --------------------------------------------------

        maintenance_days = (
            row["Days_Since_Maintenance"]
        )

        if pd.notna(maintenance_days):

            if maintenance_days > 240:

                score += 2

                reasons.append(
                    "Maintenance overdue"
                )

            elif maintenance_days > 180:

                score += 1

                reasons.append(
                    "Maintenance aging"
                )


        # --------------------------------------------------
        # PRIORITY LEVEL
        # --------------------------------------------------

        if score >= 7:

            priority = "IMMEDIATE"

        elif score >= 4:

            priority = "HIGH"

        elif score >= 2:

            priority = "MEDIUM"

        else:

            priority = "ROUTINE"


        priorities.append(
            {
                "Machine_ID": row["Machine_ID"],

                "Machine_Name": row["Machine_Name"],

                "Location": row["Location"],

                "Health_Status": row["Health_Status"],

                "Temperature": (
                    round(float(temperature), 2)
                    if pd.notna(temperature)
                    else "N/A"
                ),

                "Vibration": (
                    round(float(vibration), 2)
                    if pd.notna(vibration)
                    else "N/A"
                ),

                "Runtime_Hours": (
                    int(runtime)
                    if pd.notna(runtime)
                    else "N/A"
                ),

                "Days_Since_Maintenance": (
                    int(maintenance_days)
                    if pd.notna(maintenance_days)
                    else "N/A"
                ),

                "Maintenance_Priority": priority,

                "Reasons": reasons
            }
        )


    # ------------------------------------------------------
    # CREATE RESULT
    # ------------------------------------------------------

    result = pd.DataFrame(
        priorities
    )


    # ------------------------------------------------------
    # SORT PRIORITY
    # ------------------------------------------------------

    priority_order = {
        "IMMEDIATE": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "ROUTINE": 3
    }

    result["Priority_Order"] = result[
        "Maintenance_Priority"
    ].map(priority_order)

    result = result.sort_values(
        "Priority_Order"
    )


    # ------------------------------------------------------
    # TOP PRIORITY MACHINES
    # ------------------------------------------------------

    top_machines = result.head(15)


    return top_machines[
        [
            "Machine_ID",
            "Machine_Name",
            "Location",
            "Health_Status",
            "Temperature",
            "Vibration",
            "Runtime_Hours",
            "Days_Since_Maintenance",
            "Maintenance_Priority",
            "Reasons"
        ]
    ].to_string(
        index=False
    )