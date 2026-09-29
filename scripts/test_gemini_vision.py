import os 
from pathlib import Path    

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.schemas.image_metadata import ImageMetadata

load_dotenv()

api_key = os.environ["GEMINI_API_KEY"]

client = genai.Client(api_key=api_key)

image_path = sorted(
    path
    for path in Path("data/images").rglob("*")
    if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
)

if not image_path:
    raise FileNotFoundError("No supported images found inside data/images")

image_path = image_path[0]

prompt = """ 
Analyze this image for an article-to-image matching engine.

Identify the visually central, specific subject. Do not infer details that are not visible.
Use a broad category such as animal, person, landscape, food, vehicle, or object. Provide factual,
searchable attributes and a short factual caption. Set confidence from 0.0 to 1.0 based on how clearly
the main subject can be identified.
""" 

with image_path.open("rb") as image_file:
    image_bytes = image_file.read()

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[
        types.Part.from_bytes(
            data=image_bytes,
            mime_type=f"image/{image_path.suffix.lower().lstrip('.')}",
        ),
        prompt,
    ],
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=ImageMetadata,
    ),
)

metadata = response.parsed

if not isinstance(metadata, ImageMetadata):
    metadata = ImageMetadata.model_validate(metadata)

print(f"Image: {image_path.as_posix()}")
print(metadata.model_dump_json(indent=2))
