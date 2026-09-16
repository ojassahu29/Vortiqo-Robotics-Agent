from dataclasses import dataclass

from vortiqo.agent.world_state import WorldState
from vortiqo.language.goal import Goal


@dataclass
class TaskContext:
    """
    Shared context for the current task.

    Contains the human's goal and the agent's current
    understanding of the world.
    """

    goal: Goal
    world_state: WorldState