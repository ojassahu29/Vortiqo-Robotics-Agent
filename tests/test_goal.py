from vortiqo.language.goal import Goal


print("Creating goal...")

goal = Goal(
    action="clean",
    target="table",
)

print()
print("==========================================")
print("                 GOAL")
print("==========================================")
print(f"Action: {goal.action}")
print(f"Target: {goal.target}")
print()
print("Goal test completed.")