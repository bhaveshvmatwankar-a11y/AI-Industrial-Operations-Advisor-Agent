import pandas as pd


# ==========================================================
# STANDARD MACHINE SCHEMA
# ==========================================================

STANDARD_MACHINE_COLUMNS = {
    "Machine_ID": [
        "machine_id",
        "machineid",
        "asset_id",
        "asset_no",
        "asset_number",
        "equipment_id"
    ],

    "Machine_Name": [
        "machine_name",
        "machinename",
        "machine",
        "equipment",
        "equipment_name",
        "asset_name"
    ],

    "Location": [
        "location",
        "area",
        "section",
        "zone",
        "department"
    ],

    "Temperature": [
        "temperature",
        "temp",
        "temp_c",
        "temperature_c"
    ],

    "Pressure": [
        "pressure",
        "pressure_bar",
        "pressure_psi"
    ],

    "Vibration": [
        "vibration",
        "vibration_rms",
        "vib_rms",
        "vib_level",
        "vibration_level"
    ],

    "Current": [
        "current",
        "current_a",
        "ampere",
        "amperage"
    ],

    "Runtime_Hours": [
        "runtime",
        "runtime_hours",
        "operating_hours",
        "hours",
        "hours_used"
    ],

    "Last_Maintenance": [
        "last_maintenance",
        "last_service",
        "service_date",
        "maintenance_date"
    ],

    "Health_Status": [
        "health_status",
        "health",
        "status",
        "condition",
        "machine_status"
    ]
}


# ==========================================================
# NORMALIZE COLUMN NAME
# ==========================================================

def normalize_column_name(column):

    return (
        str(column)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


# ==========================================================
# AUTOMATIC COLUMN DETECTION
# ==========================================================

def detect_machine_columns(df):

    detected = {}

    normalized_columns = {
        normalize_column_name(column): column
        for column in df.columns
    }

    for standard_name, possible_names in STANDARD_MACHINE_COLUMNS.items():

        for possible_name in possible_names:

            if possible_name in normalized_columns:

                detected[standard_name] = (
                    normalized_columns[possible_name]
                )

                break

    return detected


# ==========================================================
# APPLY COLUMN MAPPING
# ==========================================================

def apply_machine_mapping(df, mapping):

    rename_map = {
        original_name: standard_name
        for standard_name, original_name in mapping.items()
    }

    normalized_df = df.rename(
        columns=rename_map
    ).copy()

    return normalized_df