import streamlit as st

from Agent import agent

@st.cache_resource
def load_agent():
    from Agent import agent
    return agent


agent = load_agent()



st.title("🏭 Industrial Operations Advisor AI")

st.write(
"""
AI assistant for:
- Machine monitoring
- Predictive maintenance
- Operational insights
"""
)


user_input = st.chat_input(
    "Ask about your factory machines..."
)


if user_input:

    with st.chat_message("user"):
        st.write(user_input)


    response = agent.invoke(
        {
            "messages":[
                (
                    "user",
                    user_input
                )
            ]
        }
    )

    message = response["messages"][-1].content

    if isinstance(message, list):
        answer = message[0]["text"]
    else:
        answer = message

    with st.chat_message("assistant"):
        st.markdown(answer)