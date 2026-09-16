from vortiqo.agent.world_state import WorldObject
from vortiqo.perception.sam3_perception import Scene


def scene_to_world_objects(scene: Scene) -> list[WorldObject]:
    """Convert perception results into the agent's world representation."""

    world_objects = []

    for obj in scene.objects:
        world_object = WorldObject(
            label=obj.label,
            confidence=obj.confidence,
            bbox=obj.bbox,
            center=obj.center,
            mask=obj.mask,
            mask_area=obj.mask_area,
        )

        world_objects.append(world_object)

    return world_objects