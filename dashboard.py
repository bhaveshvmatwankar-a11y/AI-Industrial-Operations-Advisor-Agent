import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="AI Industrial Operations Advisor",
    layout="wide"
)

st.title("AI Industrial Operations Advisor")
st.subheader("Real-time Machine Monitoring Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/sample_machine_data.csv"
    )


df = load_data()

st.write("Dataset Preview")

st.dataframe(df.head())


total_machines = len(df)

healthy_count = len(
    df[df["Health_Status"] == "Healthy"]
)

warning_count = len(
    df[df["Health_Status"] == "Warning"]
)

critical_count = len(
    df[df["Health_Status"] == "Critical"]
)

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

health_distribution = (
    df["Health_Status"]
    .value_counts()
    .reset_index()
)

health_distribution.columns = [
    "Status",
    "Count"
]

st.subheader("Machine Health Distribution")

fig = px.pie(
    health_distribution,
    names="Status",
    values="Count",
    title="Current Machine Health"
)

st.plotly_chart(fig)

location_data = (
    df["Location"]
    .value_counts()
    .reset_index()
)

location_data.columns = [
    "Location",
    "Machines"
]

st.subheader("Machines by Location")


fig2 = px.bar(
    location_data,
    x="Location",
    y="Machines",
    title="Factory Machine Distribution"
)


st.plotly_chart(fig2)



st.subheader(" ----Machine Inspection----")


selected_machine = st.selectbox(
    "Select Machine ID",
    df["Machine_ID"]
)

machine_data = df[
    df["Machine_ID"] == selected_machine
]

st.write("### Machine Details")

row = machine_data.iloc[0]


col1, col2, col3 = st.columns(3)


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
        "Status",
        row["Health_Status"]
    )
