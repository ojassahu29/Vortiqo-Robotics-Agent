from pathlib import Path

from PIL import Image

from vortiqo.agent.world_state import WorldState
from vortiqo.perception.sam3_perception import SAM3Perception


# --------------------------------------------------
# 1. Locate test image
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

image_path = PROJECT_ROOT / "tests" / "sam3_test_image.png"

print(f"Loading image: {image_path}")


# --------------------------------------------------
# 2. Load image
# --------------------------------------------------

image = Image.open(image_path).convert("RGB")

print(f"Image size: {image.size}")


# --------------------------------------------------
# 3. Initialize perception
# --------------------------------------------------

print()
print("Initializing SAM3 perception...")

perception = SAM3Perception()


# --------------------------------------------------
# 4. Detect objects
# --------------------------------------------------

prompts = [
    "a red object",
    "a blue object",
    "a green object",
]

print()
print("Detecting objects...")

scene = perception.detect_scene(
    image=image,
    prompts=prompts,
)


# --------------------------------------------------
# 5. Create world state
# --------------------------------------------------

print()
print("Creating world state...")

world_state = WorldState()

world_state.update(scene.objects)

# --------------------------------------------------
# 6. Display world state
# --------------------------------------------------

print()
print("==========================================")
print("             WORLD STATE")
print("==========================================")

print(f"Objects currently known: {world_state.object_count()}")

for i, obj in enumerate(world_state.objects):

    print()
    print(f"Object {i + 1}")
    print(f"  Label: {obj.label}")
    print(f"  Confidence: {obj.confidence:.3f}")
    print(f"  Center: ({obj.center[0]:.1f}, {obj.center[1]:.1f})")
    print(f"  Mask area: {obj.mask_area} pixels")


print()
print("World state test completed.")