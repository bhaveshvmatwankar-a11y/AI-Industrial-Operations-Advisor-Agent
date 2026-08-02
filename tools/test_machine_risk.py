from machine_risk_tool import check_machine_risk

result = check_machine_risk.invoke({
    "machine_id": "M001"
})

print(result)
