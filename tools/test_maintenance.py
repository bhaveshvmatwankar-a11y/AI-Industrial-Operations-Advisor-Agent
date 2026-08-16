from maintenance_tracker import get_maintenance_progress


progress = get_maintenance_progress()

print("\nMAINTENANCE PROGRESS")
print("====================")

print(
    "Total:",
    progress["Total"]
)

print(
    "Completed:",
    progress["Completed"]
)

print(
    "In Progress:",
    progress["In Progress"]
)

print(
    "Pending:",
    progress["Pending"]
)

print(
    "Progress:",
    f'{progress["Progress_Percentage"]}%'
)