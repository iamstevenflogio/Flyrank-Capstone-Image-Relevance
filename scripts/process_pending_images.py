import os 
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.models.image import ImageMetadata as ImageMetadataModel
from app.schemas.image_metadata import ImageMetadata as ImageMetadataSchema

import argparse

from sqlalchemy import select

from app.database import SessionLocal
from app.models.image import Image

DEFAULT_BATCH_SIZE = 3
MODEL_NAME = "gemini-3.8-flash"

PROMPT = """
Analyze this image for an article-to-image matching engine.

Identify the visually central, specific subject. Do not infer details that are not visible.
Use a broad category such as animal, person, landscape, food, vehicle, or object. Provide factual,
searchable attributes and a short factual caption. Set confidence from 0.0 to 1.0 based on how clearly
the main subject can be identified.

"""

def get_mime_type(image_path: Path) -> str:
    extension = image_path.suffix.lower()

    if extension == ".jpg":
        extension = ".jpeg"
    return f"image/{extension.lstrip('.')}"

def get_pending_images(batch_size: int) -> list[Image]:
    with SessionLocal() as session:
        return list(
            session.scalars(
                select(Image)
                .where(Image.status == "pending")
                .order_by(Image.id)
                .limit(batch_size)
            )
        )

def main():
    parser = argparse.ArgumentParser(
        description="Select pending images for processing."
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help="Maximum number of pending images to select.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show selected images without calling Gemini or changing the database.",
    )
    args = parser.parse_args()
    load_dotenv()
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    if args.batch_size < 1:
        raise ValueError("--batch-size must be at least 1")

    images = get_pending_images(args.batch_size)

    if not images:
        print("No pending images remain")
        return

    if args.dry_run:
        print(f"Dry run: selected {len(images)} pending image(s).")

        for image in images:
            print(
                f"id={image.id} | "
                f"filename={image.filename} | "
                f"status={image.status} | "
                f"attempts={image.attempts}"
            )
        return

    print(f"Starting real processing for {len(images)} image(s).")

    for selected_image in images:
        with SessionLocal() as session:
            image = session.get(Image, selected_image.id)
            image_path = Path(image.file_path)

            image.attempts += 1
            session.commit()

            if not image_path.exists():
                image.status = "failed"
                image.error_message = f"File not found: {image.file_path}"
                session.commit()

                print(f"Failed {image.id}: image file was not found.")
                continue

            try: 
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=[
                        types.Part.from_bytes(
                            data=image_path.read_bytes(),
                            mime_type=get_mime_type(image_path),
                        ),
                        PROMPT,
                    ],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=ImageMetadataSchema,

automatic_function_calling=types.AutomaticFunctionCallingConfig(
                            disable=True,
                        ),
                    ),
                )

                metadata = response.parsed

                if not isinstance(metadata, ImageMetadataSchema):
                    metadata = ImageMetadataSchema.model_validate(metadata)

                session.add(
                    ImageMetadataModel(
                        image_id=image.id,
                        subject=metadata.subject,
                        category=metadata.category,
                        attributes=metadata.attributes,
                        caption=metadata.caption,
                        confidence=metadata.confidence,
                        model_name=MODEL_NAME,
                        raw_response=metadata.model_dump(),
                    )
                )

                image.status = "completed"
                image.error_message = None
                session.commit()

                print(f"Completed {image.id}: {image.filename}")

            except Exception as error:
                session.rollback()

                print(f"\nFAILED IMAGE {selected_image.id}: {selected_image.filename}")
                print(f"Exception type: {type(error).__name__}")
                print(f"Exception repr: {error!r}")

                image = session.get(Image, selected_image.id)
                image.status = "failed"
                image.error_message = (
                    f"{type(error).__name__}: {error!r}"
                )[:1000]
                session.commit()

        
if __name__ == "__main__":
    main()