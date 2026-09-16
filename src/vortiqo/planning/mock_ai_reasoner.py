from typing import Any

from vortiqo.agent.task_context import TaskContext
from vortiqo.planning.ai_reasoner import AIReasoner
from vortiqo.planning.task_plan import PlanStep, TaskPlan


class MockAIReasoner(AIReasoner):
    """
    Mock implementation of the AI reasoning interface.

    This does not use a real AI model. It is only used to verify
    that the complete AI reasoning pipeline works correctly.
    """

    def build_input(self, context: TaskContext) -> dict[str, Any]:
        """Convert TaskContext into a model-like input structure."""

        return {
            "goal": {
                "action": context.goal.action,
                "target": context.goal.target,
            },
            "world": [
                {
                    "label": obj.label,
                    "confidence": obj.confidence,
                    "location": obj.location,
                }
                for obj in context.world_state.objects
            ],
        }

    def generate(self, model_input: dict[str, Any]) -> dict[str, Any]:
        """
        Simulate an AI model response.

        A real model will replace this method later.
        """

        return {
            "steps": [
                {
                    "action": "move",
                    "target": "red cup",
                    "destination": "shelf",
                },
                {
                    "action": "move",
                    "target": "blue plate",
                    "destination": "sink",
                },
            ]
        }

    def parse_output(self, model_output: dict[str, Any]) -> TaskPlan:
        """Convert the model response into a TaskPlan."""

        plan = TaskPlan()

        for step_data in model_output["steps"]:
            plan.add_step(
                PlanStep(
                    action=step_data["action"],
                    target=step_data["target"],
                    destination=step_data.get("destination"),
                    parameters=step_data.get("parameters", {}),
                )
            )

        return plan