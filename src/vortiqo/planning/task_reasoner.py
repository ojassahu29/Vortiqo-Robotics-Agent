from abc import ABC, abstractmethod

from vortiqo.agent.task_context import TaskContext
from vortiqo.planning.task_plan import TaskPlan


class TaskReasoner(ABC):
    """
    Interface for task-level reasoning.

    A reasoning implementation receives the current task context
    and generates a task plan.

    The reasoning itself is intentionally left to the implementation.
    """

    @abstractmethod
    def reason(self, context: TaskContext) -> TaskPlan:
        """Generate a task plan from the current task context."""
        pass