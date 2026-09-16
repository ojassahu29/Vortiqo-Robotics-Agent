from vortiqo.agent.task_context import TaskContext
from vortiqo.planning.task_plan import PlanStep, TaskPlan
from vortiqo.planning.task_reasoner import TaskReasoner


class BaselineReasoner(TaskReasoner):
    """
    Temporary deterministic reasoner used as a reference implementation.

    This is NOT the final Vortiqo reasoning system.
    """

    def reason(self, context: TaskContext) -> TaskPlan:
        plan = TaskPlan()

        for obj in context.world_state.objects:
            if obj.location == context.goal.target:
                plan.add_step(
                    PlanStep(
                        action="remove",
                        target=obj.label,
                    )
                )

        return plan