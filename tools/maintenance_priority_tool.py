import pandas as pd
from langchain.tools import tool


CSV_PATH = "data/sample_machine_data.csv"


@tool
def get_maintenance_priorities() -> str:
    """
    Identify machines that should receive maintenance attention
    based on health status, temperature, vibration, runtime,
    and time since last maintenance.
    """

    df = pd.read_csv(CSV_PATH)

    df["Last_Maintenance"] = pd.to_datetime(
        df["Last_Maintenance"]
    )

    today = pd.Timestamp.today()

    df["Days_Since_Maintenance"] = (
        today - df["Last_Maintenance"]
    ).dt.days

    priorities = []

    for _, row in df.iterrows():

        score = 0
        reasons = []

        # Health status
        if row["Health_Status"] == "Critical":
            score += 5
            reasons.append("Critical health status")

        elif row["Health_Status"] == "Warning":
            score += 3
            reasons.append("Warning health status")

        # Temperature
        if row["Temperature"] > 86:
            score += 3
            reasons.append("High temperature")

        elif row["Temperature"] > 84:
            score += 1
            reasons.append("Elevated temperature")

        # Vibration
        if row["Vibration"] > 1.6:
            score += 3
            reasons.append("High vibration")

        elif row["Vibration"] > 1.4:
            score += 1
            reasons.append("Elevated vibration")

        # Runtime
        if row["Runtime_Hours"] > 1800:
            score += 2
            reasons.append("High runtime")

        elif row["Runtime_Hours"] > 1500:
            score += 1
            reasons.append("High operating hours")

        # Maintenance age
        if row["Days_Since_Maintenance"] > 240:
            score += 2
            reasons.append("Maintenance overdue")

        elif row["Days_Since_Maintenance"] > 180:
            score += 1
            reasons.append("Maintenance aging")

        # Priority
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
                "Temperature": round(row["Temperature"], 2),
                "Vibration": round(row["Vibration"], 2),
                "Runtime_Hours": int(row["Runtime_Hours"]),
                "Days_Since_Maintenance": int(
                    row["Days_Since_Maintenance"]
                ),
                "Maintenance_Priority": priority,
                "Reasons": reasons
            }
        )

    result = pd.DataFrame(priorities)

    # Sort most urgent machines first
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

    # Return only the most important machines
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
    ].to_string(index=False)