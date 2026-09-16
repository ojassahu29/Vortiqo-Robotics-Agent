from vortiqo.agent.task_context import TaskContext
from vortiqo.agent.world_state import WorldObject, WorldState
from vortiqo.language.goal import Goal
from vortiqo.planning.reasoning_input import ReasoningInput


print("Creating reasoning input test context...")

# --------------------------------------------------
# 1. Create goal
# --------------------------------------------------

goal = Goal(
    action="clean",
    target="table",
)


# --------------------------------------------------
# 2. Create world state
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
# 4. Build reasoning input
# --------------------------------------------------

reasoning_input = ReasoningInput(
    goal_action="",
    goal_target="",
)

reasoning_input.from_context(context)


# --------------------------------------------------
# 5. Display result
# --------------------------------------------------

print()
print("==========================================")
print("           REASONING INPUT")
print("==========================================")

print(f"Goal action: {reasoning_input.goal_action}")
print(f"Goal target: {reasoning_input.goal_target}")

print()
print("Objects:")

for index, obj in enumerate(reasoning_input.objects, start=1):
    print(f"Object {index}:")
    print(f"  Label: {obj.label}")
    print(f"  Confidence: {obj.confidence}")
    print(f"  Location: {obj.location}")
    print(f"  Bounding box: {obj.bbox}")
    print(f"  Center: {obj.center}")
    print(f"  Properties: {obj.properties}")
    print()

print("Reasoning input test completed.")