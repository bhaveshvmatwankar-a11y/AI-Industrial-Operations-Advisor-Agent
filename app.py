import streamlit as st

from Agent import agent


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Industrial Operations Advisor",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <div class="app-header">

        <div class="app-title">
            🏭 Industrial Operations Advisor AI
        </div>

        <div class="app-subtitle">
            AI-powered industrial monitoring, maintenance intelligence,
            and operational decision support.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-title">
            🏭 Industrial Operations Advisor
        </div>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


    st.markdown(
        '<div class="sidebar-section">SYSTEM STATUS</div>',
        unsafe_allow_html=True
    )

    st.success("● AI Agent Online")


    st.markdown(
        '<div class="sidebar-section">CAPABILITIES</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        """
        🔧 Machine Monitoring

        🧠 Predictive Maintenance

        📚 Industrial Knowledge Search

        📊 Operational Analysis

        ⚠️ Risk Identification
        """
    )


    st.markdown(
        '<div class="sidebar-section">KNOWLEDGE SYSTEM</div>',
        unsafe_allow_html=True
    )


    st.info(
        "RAG knowledge retrieval is enabled."
    )


    st.markdown(
        """
        <div class="footer">
        AI Industrial Operations Advisor<br>
        Decision support system for industrial operations
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="app-header">

        <div class="app-title">
            🏭 Industrial Operations Advisor AI
        </div>

        <div class="app-subtitle">
            AI-powered industrial monitoring, maintenance intelligence,
            and operational decision support.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SYSTEM STATUS CARDS
# --------------------------------------------------

st.markdown(
    """
    <div class="status-container">

        <div class="status-card">

            <div class="status-title">
                SYSTEM
            </div>

            <div class="status-value">
                🟢 Online
            </div>

        </div>

        <div class="status-card">

            <div class="status-title">
                AI MODEL
            </div>

            <div class="status-value">
                Gemini 3.1 Flash Lite
            </div>

        </div>

        <div class="status-card">

            <div class="status-title">
                KNOWLEDGE
            </div>

            <div class="status-value">
                FAISS + RAG
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# WELCOME SCREEN
# --------------------------------------------------

if len(st.session_state.messages) == 0:

    st.markdown(
        """
        <div style="
            text-align: center;
            padding: 3rem 1rem;
            color: #9ca3af;
        ">

            <div style="font-size: 3rem;">
                🏭
            </div>

            <h2 style="color: white;">
                How can I assist with your industrial operations?
            </h2>

            <p>
                Ask about machine health, maintenance causes,
                operational risks, or industrial knowledge.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar="👤" if message["role"] == "user" else "🤖"
    ):

        st.markdown(
            message["content"]
        )


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

user_input = st.chat_input(
    "Ask about your factory machines..."
)


if user_input:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # Display user message
    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.markdown(
            user_input
        )


    # Generate AI response
    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        with st.spinner(
            "Analyzing industrial knowledge..."
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


            st.markdown(
                answer
            )


    # Store AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )