from Agent import agent

print("\n===== PDF AGENT TEST =====")

question = """
According to the uploaded vibration analysis document,
what problems can vibration analysis detect in rotating machinery?
"""

print("\nQuestion:")
print(question)

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    }
)

print("\n===== AGENT RESPONSE =====")

for message in response["messages"]:
    if hasattr(message, "content") and message.content:
        print(message.content)