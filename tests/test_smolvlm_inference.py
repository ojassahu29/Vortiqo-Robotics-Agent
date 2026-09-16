import json
import torch
from PIL import Image, ImageDraw
from transformers import AutoProcessor, AutoModelForImageTextToText


MODEL_ID = "HuggingFaceTB/SmolVLM2-500M-Video-Instruct"
DEVICE = "cuda"


def create_test_image():
    """Create the same controlled synthetic scene used in the earlier tests."""
    image = Image.new("RGB", (800, 600), "white")
    draw = ImageDraw.Draw(image)

    # Red rectangle — top-left
    draw.rectangle(
        [100, 150, 300, 350],
        fill="red",
    )

    # Blue circle — top-right
    draw.ellipse(
        [400, 150, 600, 350],
        fill="blue",
    )

    # Green rectangle — lower region
    draw.rectangle(
        [250, 400, 550, 520],
        fill="green",
    )

    return image


def generate_response(processor, model, image, prompt):
    """Run one prompt and return only the newly generated text."""

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                },
                {
                    "type": "text",
                    "text": prompt,
                },
            ],
        }
    ]

    text = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
    )

    inputs = processor(
        text=text,
        images=[image],
        text_kwargs={"return_tensors": "pt"},
    )

    inputs = {
        key: value.to(DEVICE) if hasattr(value, "to") else value
        for key, value in inputs.items()
    }

    with torch.inference_mode():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=200,
        )

    # Only decode tokens generated AFTER the input prompt.
    input_length = inputs["input_ids"].shape[1]

    new_tokens = generated_ids[:, input_length:]

    response = processor.batch_decode(
        new_tokens,
        skip_special_tokens=True,
    )[0].strip()

    return response


def main():
    print("Loading processor...")

    processor = AutoProcessor.from_pretrained(
        MODEL_ID,
    )

    print("Loading model...")

    model = AutoModelForImageTextToText.from_pretrained(
        MODEL_ID,
        dtype=torch.bfloat16,
    ).to(DEVICE)

    print()
    print("Model loaded successfully.")
    print(f"Device: {DEVICE}")
    print(f"GPU: {torch.cuda.get_device_name(0)}")

    image = create_test_image()

    prompts = {
        "A1 — Open description": (
            "Describe what you see in this image."
        ),

        "A2 — Literal visual inventory": (
            "List every visually distinct colored geometric shape "
            "you can directly observe in this image. "
            "Describe only what is visibly present. "
            "Do not infer what the shapes represent."
        ),

        "A3 — Object counting": (
            "How many distinct colored shapes are visibly present "
            "in this image? Give the number and briefly describe them."
        ),

        "A4 — Adversarial negative query": (
            "Is there a flag visible in this image? "
            "Answer yes or no, then briefly explain what is actually visible."
        ),

        "A5 — Structured extraction": (
            "Identify the visible objects in this image. "
            "For each object, provide its color, shape, and approximate "
            "position in the image. "
            "Do not invent objects, surfaces, scenes, or relationships "
            "that are not visibly present. "
            "Return ONLY valid JSON in this format:\n"
            "{\n"
            '  "objects": [\n'
            "    {\n"
            '      "color": "...",\n'
            '      "shape": "...",\n'
            '      "position": "..."\n'
            "    }\n"
            "  ]\n"
            "}"
        ),
    }

    results = {}

    print()
    print("=" * 70)
    print("        SMOLVLM2 CONTROLLED HALLUCINATION EXPERIMENT")
    print("=" * 70)

    for name, prompt in prompts.items():
        print()
        print("-" * 70)
        print(name)
        print("-" * 70)
        print(f"PROMPT:\n{prompt}")
        print()
        print("RESPONSE:")

        response = generate_response(
            processor,
            model,
            image,
            prompt,
        )

        results[name] = response

        print(response)

    print()
    print("=" * 70)
    print("             EXPERIMENT SUMMARY")
    print("=" * 70)

    for name, response in results.items():
        print()
        print(f"[{name}]")
        print(response)

    print()
    print("=" * 70)
    print("                 GPU MEMORY")
    print("=" * 70)
    print(f"Allocated: {torch.cuda.memory_allocated() / 1024**3:.2f} GB")
    print(f"Reserved:  {torch.cuda.memory_reserved() / 1024**3:.2f} GB")

    print()
    print("SmolVLM2 controlled experiment completed.")


if __name__ == "__main__":
    main()