from abc import ABC, abstractmethod
from typing import Any

from vortiqo.agent.task_context import TaskContext
from vortiqo.planning.task_plan import TaskPlan
from vortiqo.planning.task_reasoner import TaskReasoner


class AIReasoner(TaskReasoner):
    """
    Base interface for an AI-based task reasoning system.

    The implementation converts the current TaskContext into
    model input, runs an AI model, and converts the model output
    into a structured TaskPlan.
    """

    @abstractmethod
    def build_input(self, context: TaskContext) -> Any:
        """
        Convert TaskContext into input suitable for the AI model.
        """
        pass

    @abstractmethod
    def generate(self, model_input: Any) -> Any:
        """
        Run the AI model and return its output.
        """
        pass

    @abstractmethod
    def parse_output(self, model_output: Any) -> TaskPlan:
        """
        Convert the AI model output into a structured TaskPlan.
        """
        pass

    def reason(self, context: TaskContext) -> TaskPlan:
        """
        Run the complete AI reasoning pipeline.
        """

        model_input = self.build_input(context)

        model_output = self.generate(model_input)

        return self.parse_output(model_output)