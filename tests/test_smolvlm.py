import torch
from transformers import AutoProcessor, AutoModelForImageTextToText

MODEL_ID = "HuggingFaceTB/SmolVLM2-500M-Video-Instruct"

print("Loading processor...")
processor = AutoProcessor.from_pretrained(MODEL_ID)

print("Loading model...")
model = AutoModelForImageTextToText.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.bfloat16,
).to("cuda")

print()
print("==========================================")
print("           SMOLVLM2 STATUS")
print("==========================================")
print(f"Model: {MODEL_ID}")
print(f"Device: {next(model.parameters()).device}")
print(f"Dtype: {next(model.parameters()).dtype}")
print(f"GPU: {torch.cuda.get_device_name(0)}")
print(f"VRAM allocated: {torch.cuda.memory_allocated() / 1024**3:.2f} GB")
print(f"VRAM reserved: {torch.cuda.memory_reserved() / 1024**3:.2f} GB")
print()
print("SmolVLM2 loaded successfully.")