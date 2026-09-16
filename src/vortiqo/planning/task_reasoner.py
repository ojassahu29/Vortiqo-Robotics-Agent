from vortiqo.agent.task_context import TaskContext
from vortiqo.planning.task_plan import PlanStep, TaskPlan


class TaskReasoner:
    """
    Converts the current task context into a task-level plan.

    This is a baseline reasoning implementation.
    Later, the reasoning logic can be replaced or augmented
    with an AI-based planner.
    """

    def reason(self, context: TaskContext) -> TaskPlan:
        goal = context.goal
        world_state = context.world_state

        plan = TaskPlan()

        if goal.action == "clean":
            for obj in world_state.objects:

                # Only objects known to be on the target
                # should be considered for removal.
                if obj.location == goal.target:
                    plan.add_step(
                        PlanStep(
                            action="remove",
                            target=obj.label,
                        )
                    )

        else:
            raise ValueError(
                f"Unsupported goal action: '{goal.action}'"
            )

        return plan