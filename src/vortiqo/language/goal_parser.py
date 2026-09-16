from vortiqo.language.goal import Goal


class GoalParser:
    """Simple rule-based parser for converting natural-language instructions into Goals."""

    def parse(self, instruction: str) -> Goal:
        text = instruction.lower().strip()

        if "clean" in text or "tidy" in text or "clear" in text:
            if "table" in text:
                return Goal(
                    action="clean",
                    target="table",
                )

        raise ValueError(
            f"Could not understand instruction: '{instruction}'"
        )