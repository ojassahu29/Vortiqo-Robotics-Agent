from vortiqo.language.goal_parser import GoalParser


parser = GoalParser()

instructions = [
    "Clean the table.",
    "Can you get the table cleaned up?",
    "I want the table tidy.",
    "Please clear everything from the table.",
]


print("Testing goal parser...")

for instruction in instructions:
    goal = parser.parse(instruction)

    print()
    print(f"Instruction: {instruction}")
    print(f"  Action: {goal.action}")
    print(f"  Target: {goal.target}")


print()
print("Goal parser test completed.")