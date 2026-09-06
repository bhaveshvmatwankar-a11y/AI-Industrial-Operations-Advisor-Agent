from utils.column_mapper import detect_machine_columns


REQUIRED_MACHINE_COLUMNS = [
    "Machine_ID",
    "Machine_Name",
    "Health_Status"
]


def validate_machine_data(df):

    mapping = detect_machine_columns(df)

    missing = [
        column
        for column in REQUIRED_MACHINE_COLUMNS
        if column not in mapping
    ]

    return mapping, missing