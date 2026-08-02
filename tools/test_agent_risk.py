from Agent import agent


response = agent.invoke(
    {
        "messages": [
            (
                "user",
                "Check machine M001 and tell me its current risk."
            )
        ]
    }
)

print("\nFINAL ANSWER\n")
print(response["messages"][-1].content)