import streamlit as st
import re

import os
import shutil

import sqlite3

import pandas as pd

from Agent import agent

from RAG.pdf_retriever import build_pdf_index

from tools.company_context_tool import set_active_company_name

from utils.data_manager import (
    initialize_data,
    set_machine_data,
    get_machine_data,
    has_machine_data
)

from utils.column_mapper import (
    detect_machine_columns,
    apply_machine_mapping
)

from utils.data_validator import (
    validate_machine_data
)

from tools.maintenance_tracker import set_active_db_path


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Industrial Operations Advisor",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# CUSTOM STYLING
# ==========================================================

st.html(
    """
    <style>

    /* --------------------------------------------------
       GLOBAL
    -------------------------------------------------- */

    .stApp {
        background: #0b0d10;
    }

    [data-testid="stAppViewContainer"] {
        background: #0b0d10;
    }

    /* --------------------------------------------------
       SIDEBAR
    -------------------------------------------------- */

    [data-testid="stSidebar"] {
        background: #111318;
        border-right: 1px solid #24272d;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0.65rem;
    }

    .brand {
        font-size: 17px;
        font-weight: 600;
        color: #f1f1f1;
        padding: 4px 2px 12px 2px;
    }

    .brand-subtitle {
        font-size: 12px;
        color: #8b9098;
        margin-top: 4px;
    }

    .sidebar-label {
        font-size: 10px;
        font-weight: 600;
        color: #777d87;
        letter-spacing: 0.08em;
        margin-top: 18px;
        margin-bottom: 5px;
    }

    .capability {
        color: #b8bdc6;
        font-size: 12px;
        padding: 3px 2px;
    }

    .status-line {
        color: #b8bdc6;
        font-size: 12px;
        padding: 2px 0;
    }

    /* --------------------------------------------------
       MAIN CONTENT
    -------------------------------------------------- */

    .main-title {
        text-align: center;
        font-size: 30px;
        font-weight: 600;
        color: #f3f4f6;
        margin-top: 80px;
        margin-bottom: 8px;
    }

    .main-subtitle {
        text-align: center;
        color: #8d929b;
        font-size: 14px;
        margin-bottom: 45px;
    }

    .welcome-icon {
        text-align: center;
        font-size: 42px;
        margin-bottom: 15px;
    }

    /* --------------------------------------------------
       CHAT
    -------------------------------------------------- */

    [data-testid="stChatMessage"] {
        background: transparent;
        border: none;
    }

    [data-testid="stChatMessageContent"] {
        color: #e6e8eb;
        font-size: 15px;
        line-height: 1.65;
    }

    /* --------------------------------------------------
       CHAT INPUT
    -------------------------------------------------- */

    [data-testid="stChatInput"] {
        background: #17191e;
        border: 1px solid #30333a;
        border-radius: 14px;
    }

    [data-testid="stChatInput"] textarea {
        color: #f1f1f1;
    }

    /* --------------------------------------------------
       BUTTON
    -------------------------------------------------- */

    .stButton > button {
        border-radius: 8px;
        border: 1px solid #30333a;
        background: #17191e;
        color: #e5e7eb;
    }

    .stButton > button:hover {
        border-color: #555a63;
        background: #1d2026;
    }

    </style>
    """
)


# ==========================================================
# SESSION STATE
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "company_name" not in st.session_state:
    st.session_state.company_name = "Demo Factory"

initialize_data()


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

ACTIVE_SOURCE_FILE = os.path.join(
    UPLOAD_DIR,
    "active_data_source.txt"
)


def restore_persistent_data():

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )

    # ------------------------------------------------------
    # Restore only on the first app load
    # ------------------------------------------------------

    if st.session_state.get(
        "data_initialized",
        False
    ):
        return

    # Default source
    saved_source = "Demo Factory"

    if os.path.exists(ACTIVE_SOURCE_FILE):

        try:

            with open(
                ACTIVE_SOURCE_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                saved_source = f.read().strip()

        except Exception:

            saved_source = "Demo Factory"


    # Store source in session state
    st.session_state[
        "data_source"
    ] = saved_source


    # ------------------------------------------------------
    # Restore uploaded company data
    # ------------------------------------------------------

    if saved_source == "Upload Company Data":

        # Company name
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

                    st.session_state[
                        "company_name"
                    ] = saved_company

                    set_active_company_name(
                        saved_company
                    )

            except Exception:
                pass


        # Machine data
        if os.path.exists(
            ACTIVE_MACHINE_CSV
        ):

            try:

                saved_df = pd.read_csv(
                    ACTIVE_MACHINE_CSV
                )

                if not saved_df.empty:

                    set_machine_data(
                        saved_df
                    )

            except Exception:
                pass


        # Maintenance DB
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
                    st.session_state[
                        "maintenance_db_path"
                    ] = saved_db_path

                    set_active_db_path(saved_db_path)

            except Exception:
                pass


    # ------------------------------------------------------
    # Mark initialization complete
    # ------------------------------------------------------

    st.session_state[
        "data_initialized"
    ] = True


restore_persistent_data()

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.html(
        """
        <div class="brand">
            🏭 Industrial Operations Advisor
            <div class="brand-subtitle">
                AI-powered factory intelligence
            </div>
        </div>
        """
    )

    if st.button(
        "＋  New Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.html(
        """
        <div class="sidebar-label">ASSISTANT</div>
        <div class="capability">AI Agent · Online</div>
        <div class="capability">Machine & Maintenance Analysis</div>
        <div class="capability">Industrial PDF · RAG</div>
        """
    )

# ======================================================
# DATA & KNOWLEDGE
# ======================================================

with st.expander("⚙ Data & Knowledge", expanded=False):

    # ======================================================
    # FACTORY DATA
    # ======================================================

    st.markdown("### Factory Data & Knowledge")

    data_source = st.radio(
        "Select data source",
        [
            "Demo Factory",
            "Upload Company Data"
        ],
        horizontal=True,
        key="data_source"
    )

    # ==========================================================
    # HANDLE DATA SOURCE CHANGE
    # ==========================================================

    if data_source != st.session_state.get(
        "last_data_source"
    ):

        st.session_state[
            "last_data_source"
        ] = data_source

        # Save selected source
        with open(
            ACTIVE_SOURCE_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                data_source
            )

        # ------------------------------------------------------
        # SWITCH TO DEMO FACTORY
        # ------------------------------------------------------

        if data_source == "Demo Factory":

            st.session_state[
                "company_name"
            ] = "Demo Factory"

            set_active_company_name(
                "Demo Factory"
            )

            # Clear uploaded machine data
            st.session_state.pop(
                "machine_data",
                None
            )

            # Activate demo database
            st.session_state[
                "maintenance_db_path"
            ] = "data/maintenance.db"


        # ------------------------------------------------------
        # SWITCH TO UPLOADED COMPANY
        # ------------------------------------------------------

        else:

            # Restore uploaded company name
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

                    set_active_company_name(
                        saved_company
                    )


            # Restore uploaded machine data
            if os.path.exists(
                ACTIVE_MACHINE_CSV
            ):

                uploaded_df = pd.read_csv(
                    ACTIVE_MACHINE_CSV
                )

                set_machine_data(
                    uploaded_df
                )


            # Restore uploaded DB
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
                    and os.path.exists(
                        saved_db_path
                    )
                ):
                    st.session_state[
                        "maintenance_db_path"
                    ] = saved_db_path

                    set_active_db_path(
                        saved_db_path
                    )




    # ==========================================================
    # UPDATE ACTIVE DATA SOURCE
    # ==========================================================




    # ======================================================
    # DEMO FACTORY
    # ======================================================

    if data_source == "Demo Factory":

        st.markdown("### Demo Factory")

        demo_csv_path = "data/sample_machine_data.csv"
        demo_db_path = "data/maintenance.db"

        try:

            # ----------------------------------------------
            # Load demo machine data
            # ----------------------------------------------

            demo_df = pd.read_csv(
                demo_csv_path
            )

            demo_df = demo_df.dropna(
                how="all"
            )

            set_machine_data(
                demo_df
            )


            # ----------------------------------------------
            # Activate demo database
            # ----------------------------------------------

            demo_db_path = "data/maintenance.db"

            st.session_state[
                "maintenance_db_path"
            ] = demo_db_path

            set_active_db_path(
                demo_db_path
            )


            # ----------------------------------------------
            # Activate demo company
            # ----------------------------------------------

            st.session_state[
                "company_name"
            ] = "Demo Factory"

            set_active_company_name(
                "Demo Factory"
            )


            # ----------------------------------------------
            # Save active source
            # ----------------------------------------------

            with open(
                ACTIVE_SOURCE_FILE,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(
                    "Demo Factory"
                )


            st.success(
                f"✓ {len(demo_df)} machines loaded"
            )

            st.caption(
                "Using built-in demo machine data "
                "and maintenance database."
            )

        except Exception as e:

            st.error(
                f"Unable to load demo data: {e}"
            )
    # ======================================================
    # UPLOAD COMPANY DATA
    # ======================================================

    if data_source == "Upload Company Data":


        st.markdown("### Company Information")

        if "company_name" not in st.session_state:
            st.session_state["company_name"] = ""

        company_name_input = st.text_input(
            "Company Name",
            value=st.session_state["company_name"],
            placeholder="Enter company name",
            key="company_name_input"
        )

        # Store the company name centrally
        if company_name_input.strip():
            company_name = company_name_input.strip()

            st.session_state["company_name"] = company_name

            set_active_company_name(
                company_name
            )

            # Save company name permanently
            os.makedirs(
                UPLOAD_DIR,
                exist_ok=True
            )

            with open(
                    ACTIVE_COMPANY_FILE,
                    "w",
                    encoding="utf-8"
            ) as f:
                f.write(company_name)

        if st.session_state["company_name"]:
            st.caption(
                f"Uploading data for: "
                f"**{st.session_state['company_name']}**"
            )


        # ==================================================
        # MACHINE CSV
        # ==================================================

        st.markdown("### Machine Data")

        machine_file = st.file_uploader(
            "Upload Machine Data (CSV)",
            type=["csv"],
            key="machine_upload"
        )


        if machine_file is not None:

            try:

                # ------------------------------------------
                # READ CSV
                # ------------------------------------------

                df = pd.read_csv(machine_file)

                # Remove completely empty rows
                df = df.dropna(how="all")


                # ------------------------------------------
                # VALIDATE CSV
                # ------------------------------------------

                mapping, missing = validate_machine_data(df)


                if missing:

                    st.error(
                        "Missing required columns: "
                        + ", ".join(missing)
                    )

                else:

                    # --------------------------------------
                    # NORMALIZE CSV
                    # --------------------------------------

                    normalized_df = apply_machine_mapping(
                        df,
                        mapping
                    )


                    # --------------------------------------
                    # STORE MACHINE DATA
                    # --------------------------------------

                    # --------------------------------------
                    # STORE MACHINE DATA
                    # --------------------------------------

                    set_machine_data(
                        normalized_df
                    )

                    # --------------------------------------
                    # SAVE MACHINE DATA PERMANENTLY
                    # --------------------------------------

                    os.makedirs(
                        UPLOAD_DIR,
                        exist_ok=True
                    )

                    normalized_df.to_csv(
                        ACTIVE_MACHINE_CSV,
                        index=False
                    )

                    with open(
                            ACTIVE_SOURCE_FILE,
                            "w",
                            encoding="utf-8"
                    ) as f:

                        f.write(
                            "Upload Company Data"
                        )

                    # Store company name
                    if company_name.strip():

                        st.session_state[
                            "company_name"
                        ] = company_name.strip()


                    st.success(
                        f"✓ {len(normalized_df)} machines loaded"
                    )

                    st.caption(
                        "Company machine data is active."
                    )


            except Exception as e:

                st.error(
                    f"Unable to load machine data: {e}"
                )


        # ==================================================
        # MAINTENANCE DATABASE
        # ==================================================

        st.markdown("### Maintenance Data")

        maintenance_file = st.file_uploader(
            "Upload Maintenance Database",
            type=[
                "db",
                "sqlite",
                "sqlite3"
            ],
            key="maintenance_upload"
        )


        if maintenance_file is not None:

            try:

                # ------------------------------------------
                # CREATE UPLOAD DIRECTORY
                # ------------------------------------------

                os.makedirs(
                    "data/uploads",
                    exist_ok=True
                )


                # ------------------------------------------
                # SAVE DATABASE
                # ------------------------------------------

                maintenance_db_path = os.path.join(
                    "data",
                    "uploads",
                    maintenance_file.name
                )


                with open(
                    maintenance_db_path,
                    "wb"
                ) as f:

                    f.write(
                        maintenance_file.getbuffer()
                    )


                # ------------------------------------------
                # VERIFY SQLITE DATABASE
                # ------------------------------------------

                conn = sqlite3.connect(
                    maintenance_db_path
                )


                tables = pd.read_sql_query(
                    """
                    SELECT name
                    FROM sqlite_master
                    WHERE type='table'
                    """,
                    conn
                )


                # ------------------------------------------
                # CHECK MAINTENANCE TABLE
                # ------------------------------------------

                if "maintenance" not in tables["name"].values:

                    conn.close()

                    st.error(
                        "Uploaded database does not contain "
                        "a 'maintenance' table."
                    )

                    st.session_state.pop(
                        "maintenance_db_path",
                        None
                    )

                else:

                    # --------------------------------------
                    # ACTIVATE DATABASE
                    # --------------------------------------

                    st.session_state[
                        "maintenance_db_path"
                    ] = maintenance_db_path

                    set_active_db_path(
                        maintenance_db_path
                    )

                    # Save active DB path permanently

                    with open(
                            ACTIVE_DB_FILE,
                            "w",
                            encoding="utf-8"
                    ) as f:

                        f.write(
                            maintenance_db_path
                        )


                    # --------------------------------------
                    # COUNT RECORDS
                    # --------------------------------------

                    maintenance_count = pd.read_sql_query(
                        """
                        SELECT COUNT(*) AS count
                        FROM maintenance
                        """,
                        conn
                    ).iloc[0]["count"]


                    conn.close()


                    st.success(
                        "✓ Maintenance database loaded"
                    )


                    st.caption(
                        f"{maintenance_count} maintenance "
                        "records available to the AI agent."
                    )


                    # --------------------------------------
                    # COMPANY STATUS
                    # --------------------------------------

                    if company_name.strip():

                        st.info(
                            f" AI agent is using data for "
                            f"**{company_name.strip()}**"
                        )

                    else:

                        st.info(
                            "AI agent is using the uploaded "
                            "machine data and maintenance database."
                        )


            except Exception as e:

                st.error(
                    f"Unable to load maintenance database: {e}"
                )


    # INDUSTRIAL KNOWLEDGE PDF
    # ==================================================

    st.markdown("### Industrial Knowledge")

    pdf_file = st.file_uploader(
        "Upload Industrial Knowledge PDF",
        type=["pdf"],
        key="industrial_pdf_upload"
    )

    if pdf_file is not None:

        try:

            # ------------------------------------------
            # CREATE UPLOAD DIRECTORY
            # ------------------------------------------

            os.makedirs(
                "data/uploads",
                exist_ok=True
            )

            # ------------------------------------------
            # SAVE PDF
            # ------------------------------------------

            pdf_path = os.path.join(
                "data",
                "uploads",
                pdf_file.name
            )

            with open(
                pdf_path,
                "wb"
            ) as f:

                f.write(
                    pdf_file.getbuffer()
                )

            # ------------------------------------------
            # CHECK IF PDF HAS CHANGED
            # ------------------------------------------

            pdf_marker = (
                pdf_file.name,
                pdf_file.size
            )

            if st.session_state.get(
                "active_pdf_marker"
            ) != pdf_marker:

                with st.spinner(
                    "Processing industrial PDF and building RAG knowledge base..."
                ):

                    pages, chunks = build_pdf_index(
                        pdf_path
                    )

                st.session_state[
                    "active_pdf_marker"
                ] = pdf_marker

                st.success(
                    "✓ Industrial PDF loaded successfully"
                )

                st.caption(
                    f"RAG knowledge base updated: "
                    f"{pages} pages processed, "
                    f"{chunks} chunks created."
                )

            else:

                st.success(
                    "✓ Industrial PDF is already active"
                )

                st.caption(
                    "Using the existing PDF RAG knowledge base."
                )

        except Exception as e:

            st.error(
                f"Unable to process industrial PDF: {e}"
            )

    else:

        st.info(
            "Upload an industrial maintenance "
            "or equipment document to enable "
            "PDF-based RAG."
        )

# ==========================================================
# COMPACT DATA STATUS
# ==========================================================

with st.sidebar:

    st.markdown("### Data Status")

    active_company = st.session_state.get("company_name", "Demo Factory")
    st.markdown(f"**{active_company}**")

    if has_machine_data():
        current_df = get_machine_data()
        st.markdown(f'<div class="status-line">✓ {len(current_df):,} machines</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-line">○ No machine data</div>', unsafe_allow_html=True)

    if st.session_state.get("maintenance_db_path"):
        st.markdown('<div class="status-line">✓ Maintenance database</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-line">○ No maintenance database</div>', unsafe_allow_html=True)

    if st.session_state.get("active_pdf_marker"):
        st.markdown('<div class="status-line">✓ Industrial PDF / RAG</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-line">○ No industrial PDF</div>', unsafe_allow_html=True)


# ==========================================================
# WELCOME SCREEN
# ==========================================================

if len(st.session_state.messages) == 0:

    st.html(
        """
        <div class="welcome-icon">
            🏭
        </div>

        <div class="main-title">
            How can I help with your factory?
        </div>

        <div class="main-subtitle">
            Ask about machines, maintenance, risks, or
            operational insights.
        </div>
        """
    )


# ==========================================================
# CHAT HISTORY
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar="👤" if message["role"] == "user" else "🤖"
    ):

        st.markdown(
            message["content"]
        )


# ==========================================================
# CHAT INPUT
# ==========================================================

user_input = st.chat_input(
    "Ask about your factory machines..."
)


if user_input:

    # ------------------------------------------------------
    # STORE USER MESSAGE
    # ------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # ------------------------------------------------------
    # DISPLAY USER MESSAGE
    # ------------------------------------------------------

    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.markdown(
            user_input
        )


    # ------------------------------------------------------
    # GENERATE AI RESPONSE
    # ------------------------------------------------------

    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        with st.spinner(
            "Analyzing factory data..."
        ):

            response = agent.invoke(
                {
                    "messages": [
                        (
                            "user",
                            user_input
                        )
                    ]
                }
            )


            # --------------------------------------------------
            # EXTRACT FINAL MESSAGE
            # --------------------------------------------------

            message = response[
                "messages"
            ][-1].content


            if isinstance(
                message,
                list
            ):

                answer = message[0][
                    "text"
                ]

            else:

                answer = message


            # --------------------------------------------------
            # REMOVE STREAMLIT SVG ARTIFACTS
            # --------------------------------------------------





            # --------------------------------------------------
            # DISPLAY RESPONSE
            # --------------------------------------------------

            print("\n--- RAW AI RESPONSE ---")
            print(answer)
            print("--- END RAW RESPONSE ---\n")

            st.markdown(
                answer,
                anchors=False
            )


    # ------------------------------------------------------
    # STORE AI RESPONSE
    # ------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
