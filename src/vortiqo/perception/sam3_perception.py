from dataclasses import dataclass, field
from typing import Any

import torch
from PIL import Image

# pyrefly: ignore [missing-import]
from sam3.model_builder import build_sam3_image_model
# pyrefly: ignore [missing-import]
from sam3.model.sam3_image_processor import Sam3Processor


@dataclass
class SceneObject:
    """Structured representation of an object detected by SAM3."""

    label: str
    confidence: float

    bbox: list[float]
    center: list[float]

    mask: Any
    mask_area: int


@dataclass
class Scene:
    """Collection of objects detected in a scene."""

    objects: list[SceneObject] = field(default_factory=list)

    def add_object(self, obj: SceneObject) -> None:
        """Add an object to the scene."""
        self.objects.append(obj)

    def __len__(self) -> int:
        """Return the number of objects in the scene."""
        return len(self.objects)


class SAM3Perception:
    """SAM3-based visual perception module."""

    def __init__(self, device: str | None = None):
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        self.device = device

        print(f"Initializing SAM3 on: {self.device}")

        if self.device == "cuda":
            print(
                f"GPU: {torch.cuda.get_device_name(0)}"
            )

        self.model = build_sam3_image_model(
            device=self.device,
            load_from_HF=True,
        )

        self.processor = Sam3Processor(self.model)

        print("SAM3 initialized successfully.")

    def detect(
        self,
        image: Image.Image,
        prompt: str,
    ) -> list[SceneObject]:
        """
        Detect objects in an image using a natural-language prompt.

        Args:
            image: Input RGB image.
            prompt: Natural-language description of the object/concept.

        Returns:
            A list of SceneObject instances.
        """

        image = image.convert("RGB")

        with torch.autocast(
            device_type="cuda",
            dtype=torch.bfloat16,
        ):
            inference_state = self.processor.set_image(image)

            output = self.processor.set_text_prompt(
                state=inference_state,
                prompt=prompt,
            )

        boxes = output["boxes"]
        scores = output["scores"]
        masks = output["masks"]

        detected_objects: list[SceneObject] = []

        for i in range(len(scores)):

            box = boxes[i].detach().cpu().tolist()

            x1, y1, x2, y2 = box

            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            confidence = scores[i].item()

            mask = masks[i, 0].detach().cpu().clone()

            mask_area = int(mask.sum().item())

            detected_object = SceneObject(
                label=prompt,
                confidence=confidence,
                bbox=[x1, y1, x2, y2],
                center=[center_x, center_y],
                mask=mask,
                mask_area=mask_area,
            )

            detected_objects.append(detected_object)

        return detected_objects

    def detect_scene(
        self,
        image: Image.Image,
        prompts: list[str],
    ) -> Scene:
        """
        Detect multiple object concepts in an image.

        Args:
            image: Input RGB image.
            prompts: Natural-language descriptions to search for.

        Returns:
            A Scene containing all detected objects.
        """

        image = image.convert("RGB")

        # Encode the image only once.
        with torch.autocast(
            device_type="cuda",
            dtype=torch.bfloat16,
        ):
            inference_state = self.processor.set_image(image)

        scene = Scene()

        for prompt in prompts:

            with torch.autocast(
                device_type="cuda",
                dtype=torch.bfloat16,
            ):
                output = self.processor.set_text_prompt(
                    state=inference_state,
                    prompt=prompt,
                )

            boxes = output["boxes"]
            scores = output["scores"]
            masks = output["masks"]

            for i in range(len(scores)):

                box = boxes[i].detach().cpu().tolist()

                x1, y1, x2, y2 = box

                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2

                confidence = scores[i].item()

                mask = masks[i, 0].detach().cpu().clone()

                mask_area = int(mask.sum().item())

                detected_object = SceneObject(
                    label=prompt,
                    confidence=confidence,
                    bbox=[x1, y1, x2, y2],
                    center=[center_x, center_y],
                    mask=mask,
                    mask_area=mask_area,
                )

                scene.add_object(detected_object)

        return scene