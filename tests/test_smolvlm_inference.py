import torch
from PIL import Image, ImageDraw
from transformers import AutoProcessor, AutoModelForImageTextToText

MODEL_ID = "HuggingFaceTB/SmolVLM2-500M-Video-Instruct"

print("Loading processor...")
processor = AutoProcessor.from_pretrained(MODEL_ID)

print("Loading model...")
model = AutoModelForImageTextToText.from_pretrained(
    MODEL_ID,
    dtype=torch.bfloat16,
).to("cuda")

# ---------------------------------------------------------
# Create a synthetic scene
# ---------------------------------------------------------

image = Image.new("RGB", (800, 600), "white")
draw = ImageDraw.Draw(image)

draw.rectangle((100, 150, 300, 350), fill="red")
draw.ellipse((400, 150, 600, 350), fill="blue")
draw.rectangle((250, 400, 550, 520), fill="green")

# ---------------------------------------------------------
# Ask SmolVLM about the scene
# ---------------------------------------------------------

messages = [
    {
        "role": "user",
        "content": [
            {"type": "image"},
            {
                "type": "text",
                "text": (
                    "Look at this image carefully. "
                    "Describe the objects you can see, including "
                    "their colors and approximate positions."
                ),
            },
        ],
    }
]

prompt = processor.apply_chat_template(
    messages,
    add_generation_prompt=True,
)

inputs = processor(
    text=prompt,
    images=[image],
    return_tensors="pt",
)

# Move tensors to GPU.
inputs = {
    key: value.to("cuda") if hasattr(value, "to") else value
    for key, value in inputs.items()
}

print()
print("Generating response...")

with torch.inference_mode():
    generated_ids = model.generate(
        **inputs,
        max_new_tokens=150,
    )

response = processor.batch_decode(
    generated_ids,
    skip_special_tokens=True,
)[0]

print()
print("==========================================")
print("             SMOLVLM2 OUTPUT")
print("==========================================")
print(response)

print()
print("==========================================")
print("             GPU MEMORY")
print("==========================================")
print(f"Allocated: {torch.cuda.memory_allocated() / 1024**3:.2f} GB")
print(f"Reserved:  {torch.cuda.memory_reserved() / 1024**3:.2f} GB")

print()
print("SmolVLM2 inference test completed.")