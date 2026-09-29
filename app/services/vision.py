from pathlib import Path
from typing import Protocol

from app.schemas.image_metadata import ImageMetadata

class VisionClient(Protocol):
    def analyze_image(self, image_path: Path) -> ImageMetadata:
        """Return validated metadata for one image."""

class NotConfiguredVisionClient:
    def analyze_image(self, image_path: Path) -> ImageMetadata:
        raise RuntimeError(
            "Vision provider is not configured. "
            "Set up GEMINI_API_KEY before running image processing."
        )
# Above class separates worker business logic from Gemini/Ollama-specific SDK code.