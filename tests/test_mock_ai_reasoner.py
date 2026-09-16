from vortiqo.agent.task_context import TaskContext
from vortiqo.agent.world_state import WorldObject, WorldState
from vortiqo.language.goal import Goal
from vortiqo.planning.mock_ai_reasoner import MockAIReasoner


print("Creating AI reasoning test context...")

# --------------------------------------------------
# 1. Create the goal
# --------------------------------------------------

goal = Goal(
    action="clean",
    target="table",
)


# --------------------------------------------------
# 2. Create the world state
# --------------------------------------------------

world_state = WorldState()

world_state.add_object(
    WorldObject(
        label="red cup",
        confidence=0.91,
        bbox=[100.0, 150.0, 200.0, 250.0],
        center=[150.0, 200.0],
        mask=None,
        mask_area=10000,
        location="table",
    )
)

world_state.add_object(
    WorldObject(
        label="blue plate",
        confidence=0.88,
        bbox=[300.0, 150.0, 400.0, 250.0],
        center=[350.0, 200.0],
        mask=None,
        mask_area=10000,
        location="table",
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
# 4. Create the AI reasoner
# --------------------------------------------------

reasoner = MockAIReasoner()


# --------------------------------------------------
# 5. Inspect the model input
# --------------------------------------------------

model_input = reasoner.build_input(context)

print()
print("==========================================")
print("              MODEL INPUT")
print("==========================================")

print(model_input)


# --------------------------------------------------
# 6. Run the complete reasoning pipeline
# --------------------------------------------------

plan = reasoner.reason(context)


# --------------------------------------------------
# 7. Display the generated plan
# --------------------------------------------------

print()
print("==========================================")
print("            GENERATED PLAN")
print("==========================================")

for index, step in enumerate(plan.steps, start=1):
    print(f"Step {index}:")
    print(f"  Action: {step.action}")
    print(f"  Target: {step.target}")
    print(f"  Destination: {step.destination}")
    print(f"  Parameters: {step.parameters}")
    print()

print(f"Total plan steps: {plan.step_count()}")


print()
print("Mock AI reasoning test completed.")