import streamlit as st

from Agent import agent


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Industrial Operations Advisor",
    page_icon="🏭",
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
        padding-top: 1rem;
    }

    .brand {
        font-size: 18px;
        font-weight: 600;
        color: #f1f1f1;
        padding: 8px 4px 18px 4px;
    }

    .brand-subtitle {
        font-size: 12px;
        color: #8b9098;
        margin-top: 4px;
    }

    .sidebar-label {
        font-size: 11px;
        font-weight: 600;
        color: #777d87;
        letter-spacing: 0.08em;
        margin-top: 28px;
        margin-bottom: 10px;
    }

    .capability {
        color: #b8bdc6;
        font-size: 13px;
        padding: 7px 4px;
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

    /* --------------------------------------------------
       FOOTER
    -------------------------------------------------- */

    .sidebar-footer {
        position: fixed;
        bottom: 18px;
        color: #686e78;
        font-size: 11px;
        line-height: 1.5;
    }

    </style>
    """
)


# ==========================================================
# SESSION STATE
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


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
        <div class="sidebar-label">
            CAPABILITIES
        </div>

        <div class="capability">🔧 Machine Monitoring</div>
        <div class="capability">🧠 Predictive Maintenance</div>
        <div class="capability">📚 Industrial Knowledge</div>
        <div class="capability">📊 Operational Analysis</div>
        <div class="capability">⚠️ Risk Identification</div>

        <div class="sidebar-label">
            SYSTEM
        </div>

        <div class="capability">
            AI Agent Online
        </div>

        <div class="capability">
            Gemini 3.1 Flash Lite
        </div>

        <div class="capability">
            FAISS + RAG
        </div>

        <div class="sidebar-footer">
            AI Industrial Operations Advisor<br>
            Decision support for industrial operations
        </div>
        """
    )


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