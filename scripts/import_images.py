from pathlib import Path

from sqlalchemy import select

from app.database import SessionLocal
from app.models.image import Image

IMAGE_ROOT = Path("data/images")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

def find_images() -> list[Path]:
    return sorted(
        path
        for path in IMAGE_ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS
    )

def main():
    if not IMAGE_ROOT.exists():
        raise FileNotFoundError(
            f"Image folder not found: {IMAGE_ROOT.resolve()}"
        )

    image_paths = find_images()

    if not image_paths:
        print(f"No supported images found in {IMAGE_ROOT.resolve()}")
        return

    added = 0
    skipped = 0

    with SessionLocal() as session:
        for image_path in image_paths:
            relative_path = image_path.resolve().relative_to(Path.cwd()).as_posix()

            existing_image = session.scalar(
                select(Image).where(Image.file_path == relative_path)
            )

            if existing_image:
                skipped += 1
                continue

            image = Image(
                filename=image_path.name,
                file_path=relative_path,
                status="pending",
            )
            session.add(image)
            added += 1 

        session.commit()

    print(f"Found: {len(image_paths)}")
    print(f"Added: {added}")
    print(f"Skipped existing: {skipped}")

if __name__ == "__main__":
    main()