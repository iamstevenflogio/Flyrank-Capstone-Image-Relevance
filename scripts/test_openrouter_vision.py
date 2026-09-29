import base64
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from app.schemas.image_metadata import ImageMetadata


load_dotenv()

api_key = os.environ["OPENROUTER_API_KEY"]
image_root = Path("data/images")
allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}

image_paths = sorted(
    path
    for path in image_root.rglob("*")
    if path.is_file() and path.suffix.lower() in allowed_extensions
)

if not image_paths:
    raise FileNotFoundError("No supported images found in data/images")

image_path = image_paths[0]
mime_type = f"image/{image_path.suffix.lower().lstrip('.')}"
image_base64 = base64.b64encode(image_path.read_bytes()).decode("utf-8")

prompt = """
Analyze this image for an article-to-image matching engine.

Return JSON only, with this exact structure:
{
  "subject": "specific central visible subject",
  "category": "broad category such as animal, person, landscape, food, vehicle, or object",
  "attributes": ["2 to 6 factual searchable attributes"],
  "caption": "one short factual sentence",
  "confidence": 0.0
}

Rules:
- Identify the visually central, most specific visible subject.
- Do not guess details that cannot be seen.
- Confidence must be from 0.0 to 1.0.
"""

payload = {
    "model": "google/gemini-3.8-flash",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt,
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{image_base64}",
                    },
                },
            ],
        }
    ],
    "response_format": {
        "type": "json_object",
    },
}

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    },
    json=payload,
    timeout=90,
)

response.raise_for_status()

content = response.json()["choices"][0]["message"]["content"]
metadata = ImageMetadata.model_validate(json.loads(content))

print(f"Image: {image_path.as_posix()}")
print(metadata.model_dump_json(indent=2))