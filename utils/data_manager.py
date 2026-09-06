import pandas as pd
import streamlit as st


# ==========================================================
# CURRENT FACTORY DATA
# ==========================================================

# This is used by Agent tools.
# Agent tools may run outside the Streamlit script thread,
# so they should NOT depend only on st.session_state.

CURRENT_MACHINE_DATA = None
CURRENT_MAINTENANCE_DATA = None


# ==========================================================
# FACTORY DATA INITIALIZATION
# ==========================================================

def initialize_data():

    global CURRENT_MACHINE_DATA
    global CURRENT_MAINTENANCE_DATA

    # ----------------------------------------------
    # Machine data
    # ----------------------------------------------

    if "machine_data" not in st.session_state:

        demo_df = pd.read_csv(
            "data/sample_machine_data.csv"
        )

        st.session_state.machine_data = demo_df

        CURRENT_MACHINE_DATA = demo_df

    else:

        CURRENT_MACHINE_DATA = (
            st.session_state.machine_data
        )

    # ----------------------------------------------
    # Maintenance data
    # ----------------------------------------------

    if "maintenance_data" not in st.session_state:

        st.session_state.maintenance_data = None

    CURRENT_MAINTENANCE_DATA = (
        st.session_state.maintenance_data
    )


# ==========================================================
# MACHINE DATA
# ==========================================================

def set_machine_data(df: pd.DataFrame):

    global CURRENT_MACHINE_DATA

    # Store for Streamlit UI
    st.session_state.machine_data = df

    # Store for Agent tools
    CURRENT_MACHINE_DATA = df


def get_machine_data():

    global CURRENT_MACHINE_DATA

    # Agent tools should use this global data.
    if CURRENT_MACHINE_DATA is not None:

        return CURRENT_MACHINE_DATA

    # Fallback
    if "machine_data" in st.session_state:

        CURRENT_MACHINE_DATA = (
            st.session_state.machine_data
        )

        return CURRENT_MACHINE_DATA

    # Final fallback: demo dataset
    CURRENT_MACHINE_DATA = pd.read_csv(
        "data/sample_machine_data.csv"
    )

    return CURRENT_MACHINE_DATA


# ==========================================================
# MAINTENANCE DATA
# ==========================================================

def set_maintenance_data(df: pd.DataFrame):

    global CURRENT_MAINTENANCE_DATA

    st.session_state.maintenance_data = df

    CURRENT_MAINTENANCE_DATA = df


def get_maintenance_data():

    global CURRENT_MAINTENANCE_DATA

    if CURRENT_MAINTENANCE_DATA is not None:

        return CURRENT_MAINTENANCE_DATA

    if "maintenance_data" in st.session_state:

        CURRENT_MAINTENANCE_DATA = (
            st.session_state.maintenance_data
        )

        return CURRENT_MAINTENANCE_DATA

    return None


# ==========================================================
# DATA STATUS
# ==========================================================

def has_machine_data():

    df = get_machine_data()

    return (
        df is not None
        and not df.empty
    )


def has_maintenance_data():

    df = get_maintenance_data()

    return (
        df is not None
        and not df.empty
    )