from vortiqo.agent.task_context import TaskContext
from vortiqo.agent.world_state import WorldObject, WorldState
from vortiqo.language.goal_parser import GoalParser
from vortiqo.planning.baseline_reasoner import BaselineReasoner


print("Creating task context...")

# --------------------------------------------------
# 1. Create the goal
# --------------------------------------------------

parser = GoalParser()
goal = parser.parse("Clean the table.")


# --------------------------------------------------
# 2. Create a world state
# --------------------------------------------------

world_state = WorldState()

# Object on the table
world_state.add_object(
    WorldObject(
        label="red object",
        confidence=0.906,
        bbox=[100.5, 150.1, 300.5, 350.4],
        center=[200.5, 250.3],
        mask=None,
        mask_area=40039,
        location="table",
    )
)

# Object on the table
world_state.add_object(
    WorldObject(
        label="blue object",
        confidence=0.855,
        bbox=[400.0, 150.4, 600.8, 350.7],
        center=[500.4, 250.5],
        mask=None,
        mask_area=31493,
        location="table",
    )
)

# Object somewhere else
world_state.add_object(
    WorldObject(
        label="green object",
        confidence=0.871,
        bbox=[250.3, 399.7, 550.2, 520.7],
        center=[400.2, 460.2],
        mask=None,
        mask_area=36113,
        location="floor",
    )
)


# --------------------------------------------------
# 3. Create TaskContext
# --------------------------------------------------

context = TaskContext(
    goal=goal,
    world_state=world_state,
)


# --------------------------------------------------
# 4. Run task reasoning
# --------------------------------------------------

# pyrefly: ignore [bad-instantiation]
reasoner = BaselineReasoner()
plan = reasoner.reason(context)


# --------------------------------------------------
# 5. Display results
# --------------------------------------------------

print()
print("==========================================")
print("             WORLD STATE")
print("==========================================")

for index, obj in enumerate(world_state.objects, start=1):
    print(
        f"Object {index}: "
        f"{obj.label} | "
        f"location={obj.location}"
    )


print()
print("==========================================")
print("              TASK CONTEXT")
print("==========================================")

print(f"Goal action: {context.goal.action}")
print(f"Goal target: {context.goal.target}")
print(f"Known objects: {context.world_state.object_count()}")


print()
print("==========================================")
print("             GENERATED PLAN")
print("==========================================")

for index, step in enumerate(plan.steps, start=1):
    print(
        f"Step {index}: "
        f"{step.action} -> {step.target}"
    )

print()
print(f"Total plan steps: {plan.step_count()}")


# --------------------------------------------------
# 6. Verify goal-aware reasoning
# --------------------------------------------------

expected_targets = {
    "red object",
    "blue object",
}

actual_targets = {
    step.target
    for step in plan.steps
}

if actual_targets == expected_targets:
    print()
    print("PASS: Only objects on the table were selected.")

else:
    print()
    print("FAIL: Planner selected an incorrect set of objects.")


print()
print("Task reasoning test completed.")