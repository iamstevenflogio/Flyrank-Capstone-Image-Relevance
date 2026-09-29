import os 
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from sqlalchemy import select

from app.database import SessionLocal
from app.models.image import Image, ImageMetadata
from app.schemas.image_metadata import ImageMetadata as ImageMetadataSchema

load_dotenv()

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

PROMPT = """
Analyze this image for an article-to-image matching engine.

Identify the visually central, specific subject. Do not infer details that are not
visible. Use a broad category such as animal, person, landscape, food, vehicle, or object.
Provide factual, searchable attributes and a short factual caption. Set confidence from 0.0 to 1.0 
based on how clearly the main subject can be identified.

"""

def get_mime_type(image_path: Path) -> str:
    extension = image_path.suffix.lower()

    if extension == ".jpg":
        extension == ".jpeg"

    return f"image/{extension.lstrip('.')}"

def main():
    api_key = os.environ["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

    with SessionLocal() as session:
        image = session.scalar(
            select(Image)
            .where(Image.status == "pending")
            .order_by(Image.id)
            .limit(1)
        )

        if image is None:
            print('No pending images remain.')
            return

        image_path = Path(image.file_path)

        if not image_path.exists():
            image.status = "failed"
            image.error_message = f"File not found: {image.file_path}"
            session.commit()
            print(f"Marked image {image.id} as failed: file not found.")
            return

        try:
            image_bytes = image_path.read_bytes()

            response = client.models.generate_content(
                model = "gemini-3.8-flash",
                contents = [
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type=get_mime_type(image_path),
                    ),
                    PROMPT,
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ImageMetadataSchema,

automatic_function_calling = types.AutomaticFunctionCallingConfig(
                        disable=True,
                    ),
                ),
            )

            metadata = response.parsed

            if not isinstance(metadata, ImageMetadataSchema):
                metadata = ImageMetadataSchema.model_validate(metadata)

            session.add(
                ImageMetadata(
                    image_id=image.id,
                    subject=metadata.subject,
                    category=metadata.category,
                    attributes=metadata.attributes,
                    caption=metadata.caption,
                    confidence=metadata.confidence,
                    model_name="gemini-3.8-flash",
                    raw_response=metadata.model_dump(),
                )
            )

            image.status = "completed"
            image.error_message = None
            session.commit()

            print(f"Completed image {image.id}: {image.filename}")
            print(metadata.model_dump_json(indent=2))

        except Exception as error:
            session.rollback()

            image = session.get(Image, image.id)
            image.status = "failed"
            image.error_message = str(error)[:1000]
            session.commit()

            print(f"Failed image {image.id}: {error}")
            raise
if __name__ == "__main__":
    main()
