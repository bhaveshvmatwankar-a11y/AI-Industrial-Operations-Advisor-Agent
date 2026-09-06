import streamlit as st
import pandas as pd
import sqlite3


import os

from utils.data_manager import get_machine_data


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Factory Dashboard",
    page_icon="",
    layout="wide"
)

# ==========================================================
# RESTORE ACTIVE DATA SOURCE
# ==========================================================

UPLOAD_DIR = "data/uploads"

ACTIVE_SOURCE_FILE = os.path.join(
    UPLOAD_DIR,
    "active_data_source.txt"
)

ACTIVE_MACHINE_CSV = os.path.join(
    UPLOAD_DIR,
    "active_machine_data.csv"
)

ACTIVE_COMPANY_FILE = os.path.join(
    UPLOAD_DIR,
    "active_company.txt"
)

ACTIVE_DB_FILE = os.path.join(
    UPLOAD_DIR,
    "active_maintenance_db.txt"
)


# ==========================================================
# DETERMINE ACTIVE SOURCE
# ==========================================================

active_source = "Demo Factory"

if os.path.exists(
    ACTIVE_SOURCE_FILE
):

    try:

        with open(
            ACTIVE_SOURCE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            active_source = f.read().strip()

    except Exception:

        active_source = "Demo Factory"


# ==========================================================
# LOAD ACTIVE DATA
# ==========================================================

if active_source == "Demo Factory":

    # ----------------------------------------------
    # Demo machine data
    # ----------------------------------------------

    demo_csv_path = "data/sample_machine_data.csv"

    try:

        df = pd.read_csv(
            demo_csv_path
        )

        df = df.dropna(
            how="all"
        )

    except Exception as e:

        st.error(
            f"Unable to load demo machine data: {e}"
        )

        st.stop()


    # ----------------------------------------------
    # Demo maintenance DB
    # ----------------------------------------------

    maintenance_db = "data/maintenance.db"


    # ----------------------------------------------
    # Demo company
    # ----------------------------------------------

    company_name = "Demo Factory"


else:

    # ----------------------------------------------
    # Uploaded company
    # ----------------------------------------------

    company_name = "Uploaded Company"

    if os.path.exists(
        ACTIVE_COMPANY_FILE
    ):

        try:

            with open(
                ACTIVE_COMPANY_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                saved_company = f.read().strip()

            if saved_company:

                company_name = saved_company

        except Exception:
            pass


    # ----------------------------------------------
    # Uploaded machine data
    # ----------------------------------------------

    if not os.path.exists(
        ACTIVE_MACHINE_CSV
    ):

        st.warning(
            "No uploaded company machine data is available."
        )

        st.stop()


    try:

        df = pd.read_csv(
            ACTIVE_MACHINE_CSV
        )

    except Exception as e:

        st.error(
            f"Unable to load company machine data: {e}"
        )

        st.stop()


    # ----------------------------------------------
    # Uploaded maintenance DB
    # ----------------------------------------------

    maintenance_db = None

    if os.path.exists(
        ACTIVE_DB_FILE
    ):

        try:

            with open(
                ACTIVE_DB_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                saved_db_path = f.read().strip()

            if (
                saved_db_path
                and os.path.exists(
                    saved_db_path
                )
            ):

                maintenance_db = saved_db_path

        except Exception:
            maintenance_db = None

# ==========================================================
# RESTORE PERSISTENT COMPANY DATA
# ==========================================================

UPLOAD_DIR = "data/uploads"

ACTIVE_MACHINE_CSV = os.path.join(
    UPLOAD_DIR,
    "active_machine_data.csv"
)

ACTIVE_COMPANY_FILE = os.path.join(
    UPLOAD_DIR,
    "active_company.txt"
)

ACTIVE_DB_FILE = os.path.join(
    UPLOAD_DIR,
    "active_maintenance_db.txt"
)


# ----------------------------------------------------------
# Restore company name
# ----------------------------------------------------------

if os.path.exists(
    ACTIVE_COMPANY_FILE
):

    with open(
        ACTIVE_COMPANY_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        saved_company = f.read().strip()

    if saved_company:

        st.session_state[
            "company_name"
        ] = saved_company


# ----------------------------------------------------------
# Restore machine data
# ----------------------------------------------------------

if os.path.exists(
    ACTIVE_MACHINE_CSV
):

    try:

        saved_df = pd.read_csv(
            ACTIVE_MACHINE_CSV
        )

        if not saved_df.empty:

            from utils.data_manager import set_machine_data

            set_machine_data(
                saved_df
            )

    except Exception:
        pass


# ----------------------------------------------------------
# Restore maintenance DB
# ----------------------------------------------------------

if os.path.exists(
    ACTIVE_DB_FILE
):

    with open(
        ACTIVE_DB_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        saved_db_path = f.read().strip()

    if (
        saved_db_path
        and os.path.exists(saved_db_path)
    ):

        st.session_state[
            "maintenance_db_path"
        ] = saved_db_path


# ==========================================================
# TITLE
# ==========================================================

st.title(" Industrial Operations Dashboard")


st.caption(
    f" Active Company: {company_name}"
)


# ==========================================================
# MACHINE DATA
# ==========================================================

# ==========================================================
# MACHINE HEALTH SUMMARY
# ==========================================================

total_machines = len(df)

healthy = len(
    df[df["Health_Status"].str.lower() == "healthy"]
)

warning = len(
    df[df["Health_Status"].str.lower() == "warning"]
)

critical = len(
    df[df["Health_Status"].str.lower() == "critical"]
)


# ==========================================================
# KPI CARDS
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Machines",
        total_machines
    )

with col2:
    st.metric(
        "Healthy",
        healthy
    )

with col3:
    st.metric(
        "Warning",
        warning
    )

with col4:
    st.metric(
        "Critical",
        critical
    )


st.divider()


# ==========================================================
# MACHINE HEALTH DISTRIBUTION
# ==========================================================

st.subheader("Machine Health Distribution")

health_data = pd.DataFrame(
    {
        "Status": [
            "Healthy",
            "Warning",
            "Critical"
        ],
        "Machines": [
            healthy,
            warning,
            critical
        ]
    }
)

st.bar_chart(
    health_data.set_index("Status")
)


# ==========================================================
# TEMPERATURE ANALYSIS
# ==========================================================

st.subheader("🌡️ Temperature by Machine")

temperature_data = df[
    ["Machine_ID", "Temperature"]
].set_index("Machine_ID")

st.bar_chart(
    temperature_data
)


# ==========================================================
# VIBRATION ANALYSIS
# ==========================================================

st.subheader("📈 Vibration by Machine")

vibration_data = df[
    ["Machine_ID", "Vibration"]
].set_index("Machine_ID")

st.bar_chart(
    vibration_data
)


# ==========================================================
# MAINTENANCE DATABASE
# ==========================================================

st.divider()

st.subheader("🔧 Maintenance Overview")

maintenance_db = st.session_state.get(
    "maintenance_db_path"
)


if maintenance_db:

    try:

        conn = sqlite3.connect(
            maintenance_db
        )

        maintenance_df = pd.read_sql_query(
            "SELECT * FROM maintenance",
            conn
        )



        conn.close()

        # ----------------------------------------------
        # MAINTENANCE STATUS COUNTS
        # ----------------------------------------------

        status_counts = (
            maintenance_df["maintenance_status"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        pending = status_counts[
            status_counts == "pending"
            ].count()

        in_progress = status_counts[
            status_counts == "in progress"
            ].count()

        completed = status_counts[
            status_counts == "completed"
            ].count()

        # ----------------------------------------------
        # MAINTENANCE STATUS CHART
        # ----------------------------------------------

        maintenance_status = pd.DataFrame(
            {
                "Status": [
                    "Pending",
                    "In Progress",
                    "Completed"
                ],
                "Tasks": [
                    pending,
                    in_progress,
                    completed
                ]
            }
        )

        st.bar_chart(
            maintenance_status.set_index(
                "Status"
            )
        )


    except Exception as e:

        st.error(
            f"Unable to read maintenance database: {e}"
        )

else:

    st.info(
        "No maintenance database is currently loaded."
    )


# ==========================================================
# CRITICAL MACHINES
# ==========================================================

st.divider()

st.subheader("⚠️ Critical Machines")

critical_df = df[
    df["Health_Status"]
    .astype(str)
    .str.lower()
    == "critical"
]


if critical_df.empty:

    st.success(
        "No critical machines detected."
    )

else:

    st.dataframe(
        critical_df,
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# COMPLETE MACHINE DATA
# ==========================================================

st.divider()

st.subheader("🏭 Machine Data")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)