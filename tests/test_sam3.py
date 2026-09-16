import torch
from PIL import Image, ImageDraw

from sam3.model_builder import build_sam3_image_model
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

# Draw some simple objects
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
# 4. Give SAM3 the image
# --------------------------------------------------

image = Image.open(image_path).convert("RGB")

print("Processing image...")

inference_state = processor.set_image(image)

print("Image processed.")


# --------------------------------------------------
# 5. Ask SAM3 to find a circle
# --------------------------------------------------

print('Asking SAM3 to find: "a circle"')

output = processor.set_text_prompt(
    state=inference_state,
    prompt="a circle",
)


# --------------------------------------------------
# 6. Get the results
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