import torch
from PIL import Image

from sam3.model_builder import build_sam3_image_model
from sam3.model.sam3_image_processor import Sam3Processor


# 1. Select the GPU if CUDA is available
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Using device: {device}")

if device == "cuda":
    print(f"GPU: {torch.cuda.get_device_name(0)}")


# 2. Load SAM3
print("Loading SAM3...")

model = build_sam3_image_model(
    device=device,
    load_from_HF=True,
)

processor = Sam3Processor(model)

print("SAM3 loaded successfully.")