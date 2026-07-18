import random
import pandas as pd
from datetime import datetime, timedelta

machine_types = [
    "CNC Machine",
    "Hydraulic Press",
    "Conveyor Belt",
    "Air Compressor",
    "Boiler",
    "Industrial Pump",
    "Assembly Robot",
    "Packaging Machine",
    "Cooling System",
    "Generator"
]

locations = [
    "Section A",
    "Section B",
    "Section C",
    "Assembly Line",
    "Warehouse",
    "Packaging Unit"
]

machine_data = []

for i in range(500):
    machine_id = f"M{i + 1:03}"

    temperature = random.uniform(55,90)

    pressure = round(random.uniform(1.5, 4.0), 2)

    vibration = random.uniform(0.1,1.8)

    current = round(random.uniform(5, 30), 2)

    runtime = random.randint(100, 2000)

    if temperature > 86 and vibration > 1.6:
        health_status = "Critical"

    elif temperature > 84 or vibration > 1.4:
        health_status = "Warning"

    else:
        health_status = "Healthy"

    maintenance_date = (
            datetime.now() - timedelta(days=random.randint(10, 300))
    ).date()

    machine_data.append(
        {
            "Machine_ID": machine_id,
            "Machine_Name": random.choice(machine_types),
            "Location": random.choice(locations),
            "Temperature": temperature,
            "Pressure": pressure,
            "Vibration": vibration,
            "Current": current,
            "Runtime_Hours": runtime,
            "Last_Maintenance": maintenance_date,
            "Health_Status": health_status
        }
    )

df = pd.DataFrame(machine_data)


df.to_csv(
    "../data/sample_machine_data.csv",
    index=False
)

print("Industrial dataset generated successfully!")
print(df.head())


print(df.shape)

