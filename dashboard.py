import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Industrial Operations Advisor",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🏭 AI Industrial Operations Advisor")
st.subheader("Real-time Machine Monitoring Dashboard")


# --------------------------------------------------
# LOAD MACHINE DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    return pd.read_csv(
        "data/sample_machine_data.csv"
    )


df = load_data()


# --------------------------------------------------
# DATASET PREVIEW
# --------------------------------------------------

st.write("### Dataset Preview")

st.dataframe(
    df.head(),
    use_container_width=True
)


# --------------------------------------------------
# MACHINE HEALTH COUNTS
# --------------------------------------------------

total_machines = len(df)

healthy_count = len(
    df[
        df["Health_Status"] == "Healthy"
    ]
)

warning_count = len(
    df[
        df["Health_Status"] == "Warning"
    ]
)

critical_count = len(
    df[
        df["Health_Status"] == "Critical"
    ]
)


# --------------------------------------------------
# MACHINE STATUS METRICS
# --------------------------------------------------

st.subheader("Machine Health Overview")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Machines",
        total_machines
    )


with col2:

    st.metric(
        "Healthy",
        healthy_count
    )


with col3:

    st.metric(
        "Warning",
        warning_count
    )


with col4:

    st.metric(
        "Critical",
        critical_count
    )


# --------------------------------------------------
# MACHINE HEALTH DISTRIBUTION
# --------------------------------------------------

health_distribution = (
    df["Health_Status"]
    .value_counts()
    .reset_index()
)

health_distribution.columns = [
    "Status",
    "Count"
]


st.subheader(
    "Machine Health Distribution"
)


fig = px.pie(
    health_distribution,
    names="Status",
    values="Count",
    title="Current Machine Health"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------------------------
# MACHINE LOCATION DISTRIBUTION
# --------------------------------------------------

location_data = (
    df["Location"]
    .value_counts()
    .reset_index()
)

location_data.columns = [
    "Location",
    "Machines"
]


st.subheader(
    "Machines by Location"
)


fig2 = px.bar(
    location_data,
    x="Location",
    y="Machines",
    title="Factory Machine Distribution"
)


st.plotly_chart(
    fig2,
    use_container_width=True
)


# --------------------------------------------------
# MACHINE INSPECTION
# --------------------------------------------------

st.subheader(
    "🔍 Machine Inspection"
)


selected_machine = st.selectbox(
    "Select Machine ID",
    df["Machine_ID"]
)


machine_data = df[
    df["Machine_ID"] == selected_machine
]


row = machine_data.iloc[0]


st.write("### Machine Details")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Temperature",
        f"{row['Temperature']:.1f} °C"
    )


with col2:

    st.metric(
        "Vibration",
        f"{row['Vibration']:.2f} mm/s"
    )


with col3:

    st.metric(
        "Pressure",
        f"{row['Pressure']:.2f}"
    )


with col4:

    st.metric(
        "Status",
        row["Health_Status"]
    )


# --------------------------------------------------
# LOAD MAINTENANCE DATABASE
# --------------------------------------------------

conn = sqlite3.connect(
    "data/maintenance.db"
)


maintenance_df = pd.read_sql_query(
    "SELECT * FROM maintenance ORDER BY id",
    conn
)


conn.close()


# --------------------------------------------------
# MAINTENANCE OVERVIEW
# --------------------------------------------------

st.subheader(
    "🔧 Maintenance Overview"
)


total_tasks = len(
    maintenance_df
)


completed_tasks = len(
    maintenance_df[
        maintenance_df[
            "maintenance_status"
        ] == "Completed"
    ]
)


in_progress_tasks = len(
    maintenance_df[
        maintenance_df[
            "maintenance_status"
        ] == "In Progress"
    ]
)


pending_tasks = len(
    maintenance_df[
        maintenance_df[
            "maintenance_status"
        ] == "Pending"
    ]
)


progress = (

    completed_tasks
    / total_tasks
    * 100

    if total_tasks > 0

    else 0
)


# --------------------------------------------------
# MAINTENANCE METRICS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Tasks",
        total_tasks
    )


with col2:

    st.metric(
        "Completed",
        completed_tasks
    )


with col3:

    st.metric(
        "In Progress",
        in_progress_tasks
    )


with col4:

    st.metric(
        "Pending",
        pending_tasks
    )


st.metric(
    "Maintenance Progress",
    f"{progress:.1f}%"
)


# --------------------------------------------------
# MAINTENANCE STATUS CHART
# --------------------------------------------------

maintenance_status = (

    maintenance_df[
        "maintenance_status"
    ]

    .value_counts()

    .reset_index()
)


maintenance_status.columns = [
    "Status",
    "Count"
]


st.subheader(
    "Maintenance Task Status"
)


fig3 = px.bar(
    maintenance_status,
    x="Status",
    y="Count",
    title="Maintenance Task Status"
)


st.plotly_chart(
    fig3,
    use_container_width=True
)


# --------------------------------------------------
# MAINTENANCE TYPE CHART
# --------------------------------------------------

maintenance_types = (

    maintenance_df[
        "maintenance_type"
    ]

    .value_counts()

    .reset_index()
)


maintenance_types.columns = [
    "Maintenance Type",
    "Count"
]


st.subheader(
    "Maintenance Activities by Type"
)


fig4 = px.pie(
    maintenance_types,
    names="Maintenance Type",
    values="Count",
    title="Maintenance Activities by Type"
)


st.plotly_chart(
    fig4,
    use_container_width=True
)


# --------------------------------------------------
# MAINTENANCE DATABASE TABLE
# --------------------------------------------------

st.subheader(
    "📋 Maintenance Records"
)


st.dataframe(
    maintenance_df,
    use_container_width=True,
    hide_index=True
)