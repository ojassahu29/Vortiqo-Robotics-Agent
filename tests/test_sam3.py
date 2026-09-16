import torch
from PIL import Image, ImageDraw

# pyrefly: ignore [missing-import]
from sam3.model_builder import build_sam3_image_model
# pyrefly: ignore [missing-import]
from sam3.model.sam3_image_processor import Sam3Processor


# --------------------------------------------------
# 1. Select the device
# --------------------------------------------------

device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Using device: {device}")

if device == "cuda":
    print(f"GPU: {torch.cuda.get_device_name(0)}")


# --------------------------------------------------
# 2. Create a simple test image
# --------------------------------------------------

image_path = r"Z:\Robotics-AI-Agent\tests\sam3_test_image.png"

image = Image.new("RGB", (800, 600), "white")
draw = ImageDraw.Draw(image)

draw.rectangle((100, 150, 300, 350), fill="red")
draw.ellipse((400, 150, 600, 350), fill="blue")
draw.rectangle((250, 400, 550, 520), fill="green")

image.save(image_path)

print(f"Test image saved to: {image_path}")


# --------------------------------------------------
# 3. Load SAM3
# --------------------------------------------------

print("Loading SAM3...")

model = build_sam3_image_model(
    device=device,
    load_from_HF=True,
)

processor = Sam3Processor(model)

print("SAM3 loaded successfully.")


# --------------------------------------------------
# 4. Give SAM3 the image and run inference
# --------------------------------------------------

image = Image.open(image_path).convert("RGB")

print("Processing image...")

with torch.autocast(device_type="cuda", dtype=torch.bfloat16):

    inference_state = processor.set_image(image)

    print("Image processed.")

    print('Asking SAM3 to find: "a circle"')

    output = processor.set_text_prompt(
        state=inference_state,
        prompt="a circle",
    )

print("Inference completed.")


# --------------------------------------------------
# 5. Get the results
# --------------------------------------------------

masks = output["masks"]
boxes = output["boxes"]
scores = output["scores"]

print()
print("========== SAM3 RESULTS ==========")
print(f"Number of detected objects: {len(scores)}")
print(f"Masks shape: {masks.shape}")
print(f"Boxes shape: {boxes.shape}")
print(f"Scores: {scores}")
print("==================================")


# --------------------------------------------------
# 6. Visualize the first detection
# --------------------------------------------------

print("Creating visualization...")

visualization = image.copy()
draw = ImageDraw.Draw(visualization)

# Get the first bounding box
box = boxes[0].detach().cpu().tolist()
x1, y1, x2, y2 = box

# Draw bounding box
draw.rectangle(
    (x1, y1, x2, y2),
    outline="yellow",
    width=5,
)

# Draw label
draw.text(
    (x1, max(0, y1 - 20)),
    f"circle: {scores[0].item():.3f}",
    fill="yellow",
)


# --------------------------------------------------
# 6. Visualize the segmentation mask
# --------------------------------------------------

print("Creating mask visualization...")

# Get the first mask from the GPU tensor
mask = masks[0, 0].detach().cpu()

# Convert mask to a NumPy array
mask = mask.numpy()

# Make sure the mask is boolean
if mask.dtype != bool:
    mask = mask > 0.5

# Create a copy of the original image
visualization = image.copy()

# Create a transparent overlay
overlay = Image.new("RGBA", visualization.size, (0, 0, 0, 0))
overlay_pixels = overlay.load()

# Color pixels belonging to the detected object
for y in range(mask.shape[0]):
    for x in range(mask.shape[1]):
        if mask[y, x]:
            overlay_pixels[x, y] = (255, 255, 0, 100)

# Combine the overlay with the original image
visualization = Image.alpha_composite(
    visualization.convert("RGBA"),
    overlay,
)

# Draw the bounding box and label
draw = ImageDraw.Draw(visualization)

box = boxes[0].detach().cpu().tolist()
x1, y1, x2, y2 = box

draw.rectangle(
    (x1, y1, x2, y2),
    outline="yellow",
    width=5,
)

draw.text(
    (x1, max(0, y1 - 20)),
    f"circle: {scores[0].item():.3f}",
    fill="yellow",
)


# --------------------------------------------------
# 7. Save visualization
# --------------------------------------------------

output_path = r"Z:\Robotics-AI-Agent\tests\sam3_mask_result.png"

visualization.save(output_path)

print(f"Mask visualization saved to: {output_path}")