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

# Red rectangle
draw.rectangle(
    (100, 150, 300, 350),
    fill="red",
)

# Blue circle
draw.ellipse(
    (400, 150, 600, 350),
    fill="blue",
)

# Green rectangle
draw.rectangle(
    (250, 400, 550, 520),
    fill="green",
)

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
# 4. Process the image
# --------------------------------------------------

image = Image.open(image_path).convert("RGB")

print("Processing image...")

with torch.autocast(
    device_type="cuda",
    dtype=torch.bfloat16,
):
    inference_state = processor.set_image(image)

print("Image processed.")


# --------------------------------------------------
# 5. Test multiple language prompts
# --------------------------------------------------

prompts = [
    "a red object",
    "a blue object",
    "a green object",
]

all_results = {}


for prompt in prompts:

    print()
    print(f'Asking SAM3: "{prompt}"')

    with torch.autocast(
        device_type="cuda",
        dtype=torch.bfloat16,
    ):
        output = processor.set_text_prompt(
            state=inference_state,
            prompt=prompt,
        )

    # --------------------------------------------------
    # IMPORTANT:
    # Make independent copies of the result tensors.
    #
    # SAM3 may reuse/mutate output tensors when the next
    # prompt is processed. clone() prevents previously
    # stored results from changing.
    # --------------------------------------------------

    stored_output = {
        "masks": output["masks"].detach().clone(),
        "boxes": output["boxes"].detach().clone(),
        "scores": output["scores"].detach().clone(),
    }

    all_results[prompt] = stored_output

    masks = stored_output["masks"]
    boxes = stored_output["boxes"]
    scores = stored_output["scores"]

    print(f"Detected objects: {len(scores)}")

    for i in range(len(scores)):

        # Move bounding box from GPU to CPU
        box = boxes[i].detach().cpu().tolist()

        x1, y1, x2, y2 = box

        # Calculate bounding-box center
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        confidence = scores[i].item()

        print(f"  Detection {i + 1}")
        print(f"    Confidence: {confidence:.3f}")
        print(
            f"    Bounding box: "
            f"[{x1:.1f}, {y1:.1f}, {x2:.1f}, {y2:.1f}]"
        )
        print(
            f"    Center: "
            f"({center_x:.1f}, {center_y:.1f})"
        )


# --------------------------------------------------
# 6. Summary
# --------------------------------------------------

print()
print("==========================================")
print("          MULTI-PROMPT SUMMARY")
print("==========================================")


for prompt, output in all_results.items():

    prompt_scores = output["scores"]
    prompt_boxes = output["boxes"]

    print()
    print(f'Prompt: "{prompt}"')
    print(f"Detections: {len(prompt_scores)}")

    for i in range(len(prompt_scores)):

        confidence = prompt_scores[i].item()

        box = prompt_boxes[i].detach().cpu().tolist()

        x1, y1, x2, y2 = box

        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        print(f"  Detection {i + 1}")
        print(f"    Confidence: {confidence:.3f}")
        print(
            f"    Bounding box: "
            f"[{x1:.1f}, {y1:.1f}, {x2:.1f}, {y2:.1f}]"
        )
        print(
            f"    Center: "
            f"({center_x:.1f}, {center_y:.1f})"
        )


print()
print("Multi-prompt SAM3 test completed.")