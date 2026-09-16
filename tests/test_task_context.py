from vortiqo.agent.task_context import TaskContext
from vortiqo.agent.world_state import WorldState
from vortiqo.language.goal_parser import GoalParser


print("Creating task context...")

# Convert the human instruction into a Goal
parser = GoalParser()
goal = parser.parse("Clean the table.")

# Create the current world state
world_state = WorldState()

# Combine the goal and world state
context = TaskContext(
    goal=goal,
    world_state=world_state,
)

print()
print("==========================================")
print("              TASK CONTEXT")
print("==========================================")
print(f"Goal action: {context.goal.action}")
print(f"Goal target: {context.goal.target}")
print(f"Known objects: {context.world_state.object_count()}")

print()
print("Task context test completed.")