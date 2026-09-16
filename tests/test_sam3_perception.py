from pathlib import Path

from PIL import Image

from vortiqo.perception.sam3_perception import SAM3Perception


# --------------------------------------------------
# 1. Locate the test image
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
# 3. Initialize SAM3 perception
# --------------------------------------------------

print()
print("Initializing SAM3 perception module...")

perception = SAM3Perception()


# --------------------------------------------------
# 4. Define concepts to search for
# --------------------------------------------------

prompts = [
    "a red object",
    "a blue object",
    "a green object",
]


# --------------------------------------------------
# 5. Build scene
# --------------------------------------------------

print()
print("Building scene...")

scene = perception.detect_scene(
    image=image,
    prompts=prompts,
)


# --------------------------------------------------
# 6. Display scene
# --------------------------------------------------

print()
print("==========================================")
print("             SCENE RESULTS")
print("==========================================")

print(f"Total detected objects: {len(scene)}")


for i, obj in enumerate(scene.objects):

    print()
    print(f"Object {i + 1}")
    print(f"  Label: {obj.label}")
    print(f"  Confidence: {obj.confidence:.3f}")

    print(
        f"  Bounding box: "
        f"[{obj.bbox[0]:.1f}, "
        f"{obj.bbox[1]:.1f}, "
        f"{obj.bbox[2]:.1f}, "
        f"{obj.bbox[3]:.1f}]"
    )

    print(
        f"  Center: "
        f"({obj.center[0]:.1f}, "
        f"{obj.center[1]:.1f})"
    )

    print(f"  Mask area: {obj.mask_area} pixels")


print()
print("SAM3 scene perception test completed.")