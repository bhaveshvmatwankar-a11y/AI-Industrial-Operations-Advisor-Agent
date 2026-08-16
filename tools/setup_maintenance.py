import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta


CSV_PATH = "data/sample_machine_data.csv"
DB_PATH = "data/maintenance.db"


# --------------------------------------------------
# LOAD MACHINE DATA
# --------------------------------------------------

df = pd.read_csv(CSV_PATH)

df["Last_Maintenance"] = pd.to_datetime(
    df["Last_Maintenance"]
)


# --------------------------------------------------
# CREATE DATABASE
# --------------------------------------------------

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute("""
    DROP TABLE IF EXISTS maintenance
""")

cursor.execute("""
    CREATE TABLE maintenance (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        machine_id TEXT NOT NULL,

        machine_name TEXT NOT NULL,

        location TEXT NOT NULL,

        health_status TEXT NOT NULL,

        maintenance_status TEXT NOT NULL,

        maintenance_date TEXT NOT NULL,

        maintenance_type TEXT NOT NULL,

        notes TEXT

    )
""")


# --------------------------------------------------
# SELECT MACHINES
# --------------------------------------------------

#random.seed(42)

# Select 40 machines from the existing dataset
selected_machines = df.sample(
    n=40
)


# --------------------------------------------------
# MAINTENANCE RECORD GENERATION
# --------------------------------------------------

for _, machine in selected_machines.iterrows():

    machine_id = machine["Machine_ID"]
    machine_name = machine["Machine_Name"]
    location = machine["Location"]
    health = machine["Health_Status"]

    temperature = machine["Temperature"]
    vibration = machine["Vibration"]
    runtime = machine["Runtime_Hours"]


    # ----------------------------------------------
    # Determine maintenance status
    # ----------------------------------------------

    if health == "Critical":

        status = random.choice([
            "Pending",
            "In Progress"
        ])

    elif health == "Warning":

        status = random.choice([
            "Pending",
            "In Progress",
            "Completed"
        ])

    else:

        status = random.choice([
            "Completed",
            "Completed",
            "Pending"
        ])


    # ----------------------------------------------
    # Determine maintenance type
    # ----------------------------------------------

    if vibration > 1.4:

        maintenance_type = "Vibration Inspection"

        notes = (
            f"Elevated vibration detected "
            f"({vibration:.2f}). Inspect bearings, "
            f"alignment and mounting components."
        )

    elif temperature > 84:

        maintenance_type = "Temperature Inspection"

        notes = (
            f"Elevated operating temperature "
            f"detected ({temperature:.1f} °C). "
            f"Inspect cooling system and operating load."
        )

    elif runtime > 1800:

        maintenance_type = "Preventive Maintenance"

        notes = (
            f"High operating runtime "
            f"({runtime} hours). Schedule preventive "
            f"inspection and servicing."
        )

    else:

        maintenance_type = "Routine Maintenance"

        notes = (
            "Routine preventive maintenance "
            "and general machine inspection."
        )


    # ----------------------------------------------
    # Maintenance date
    # ----------------------------------------------

    days_ago = random.randint(
        1,
        120
    )

    maintenance_date = (
        datetime.now()
        - timedelta(days=days_ago)
    ).date()


    # ----------------------------------------------
    # Insert record
    # ----------------------------------------------

    cursor.execute(
        """
        INSERT INTO maintenance
        (
            machine_id,
            machine_name,
            location,
            health_status,
            maintenance_status,
            maintenance_date,
            maintenance_type,
            notes
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (
            machine_id,
            machine_name,
            location,
            health,
            status,
            str(maintenance_date),
            maintenance_type,
            notes
        )
    )


# --------------------------------------------------
# SAVE DATABASE
# --------------------------------------------------

conn.commit()

conn.close()


print(
    "Realistic maintenance database "
    "generated successfully!"
)

print(
    f"Total maintenance records: "
    f"{len(selected_machines)}"
)