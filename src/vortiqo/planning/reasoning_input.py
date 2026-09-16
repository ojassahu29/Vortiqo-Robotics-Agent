from dataclasses import dataclass, field
from typing import Any

from vortiqo.agent.task_context import TaskContext


@dataclass
class ReasoningObject:
    """
    Object information provided to the reasoning system.
    """

    label: str
    confidence: float
    location: str | None = None
    bbox: list[float] | None = None
    center: list[float] | None = None
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass
class ReasoningInput:
    """
    Structured information provided to an AI reasoning system.

    This is deliberately separate from WorldState so that the
    reasoning model does not depend directly on the internal
    representation used by the perception system.
    """

    goal_action: str
    goal_target: str

    objects: list[ReasoningObject] = field(default_factory=list)

    environment: dict[str, Any] = field(default_factory=dict)

    def from_context(self, context: TaskContext) -> None:
        """
        Populate the reasoning input from the current TaskContext.
        """

        self.goal_action = context.goal.action
        self.goal_target = context.goal.target

        self.objects = [
            ReasoningObject(
                label=obj.label,
                confidence=obj.confidence,
                location=obj.location,
                bbox=obj.bbox,
                center=obj.center,
            )
            for obj in context.world_state.objects
        ]