from dataclasses import dataclass, field
from typing import Any


@dataclass
class WorldObject:
    label: str
    confidence: float
    bbox: list[float]
    center: list[float]
    mask: Any
    mask_area: int


@dataclass
class WorldState:
    objects: list[WorldObject] = field(default_factory=list)

    def update(self, objects: list[WorldObject]) -> None:
        self.objects = objects

    def add_object(self, obj: WorldObject) -> None:
        self.objects.append(obj)

    def object_count(self) -> int:
        return len(self.objects)

    def clear(self) -> None:
        self.objects.clear()