from dataclasses import dataclass, field
from typing import Any


@dataclass
class WorldObject:
    """An object currently represented in the agent's world state."""

    label: str
    confidence: float

    # Image-space information from perception
    bbox: list[float]
    center: list[float]
    mask: Any
    mask_area: int

    # Semantic information about the object's location
    location: str | None = None


@dataclass
class WorldState:
    """Current internal representation of the environment."""

    objects: list[WorldObject] = field(default_factory=list)

    def update(self, objects: list[WorldObject]) -> None:
        """Replace the current world objects."""
        self.objects = objects

    def add_object(self, obj: WorldObject) -> None:
        """Add an object to the world state."""
        self.objects.append(obj)

    def object_count(self) -> int:
        """Return the number of currently known objects."""
        return len(self.objects)

    def clear(self) -> None:
        """Clear the current world state."""
        self.objects.clear()