from vortiqo.planning.task_plan import PlanStep, TaskPlan


print("Creating task plan...")

plan = TaskPlan()

# Step with only action and target
plan.add_step(
    PlanStep(
        action="inspect",
        target="table",
    )
)

# Step with a destination
plan.add_step(
    PlanStep(
        action="move",
        target="red cup",
        destination="shelf",
    )
)

# Step with additional parameters
plan.add_step(
    PlanStep(
        action="place",
        target="blue plate",
        destination="sink",
        parameters={
            "orientation": "upright",
        },
    )
)


print()
print("==========================================")
print("              TASK PLAN")
print("==========================================")

for index, step in enumerate(plan.steps, start=1):
    print(f"Step {index}:")
    print(f"  Action: {step.action}")
    print(f"  Target: {step.target}")
    print(f"  Destination: {step.destination}")
    print(f"  Parameters: {step.parameters}")
    print()

print(f"Total steps: {plan.step_count()}")

print()
print("Task plan test completed.")