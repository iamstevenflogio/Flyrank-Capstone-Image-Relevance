from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import SessionLocal
from app.models.image import Image, ImageMetadata, AICallLog
from app.schemas.image_response import (
    AICallLogResponse,
    ImageResponse,
)

app = FastAPI(
    title="ImageMatch API",
    version="0.1.0",
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get(
    "/images",
    response_model=list[ImageResponse],
    tags=["Images"],
    summary="List images and AI metadata",
)
def list_images(
    status: str | None = None,
    category: str | None = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    query = (
        db.query(Image)
        .options(joinedload(Image.metadata_record))
        .order_by(Image.id)
    )

    if status:
        query = query.filter(Image.status == status)

    if category:
        query = query.join(Image.metadata_record).filter(
            ImageMetadata.category == category
        )

    return query.offset(offset).limit(limit).all()

@app.get(
    "/images/{image_id}",
    response_model=ImageResponse,
    tags=["Images"],
    summary="Get one image and its AI metadata",
)
def get_image(image_id: int, db: Session = Depends(get_db)):
    image = (
        db.query(Image)
        .options(joinedload(Image.metadata_record))
        .filter(Image.id == image_id)
        .one_or_none()
    )

    if image is None:
        raise HTTPException(
            status_code=404,
            detail="Image not found",
        )

    return image

@app.get(
    "/images/{image_id}/calls",
    response_model=list[AICallLogResponse],
    tags=["Images"],
    summary="List Gemini call records for one image",
)
def list_image_calls(
    image_id: int,
    db: Session = Depends(get_db),
):
    image_exists = (
        db.query(Image.id)
        .filter(Image.id == image_id)
        .first()
    )

    if image_exists is None:
        raise HTTPException(
            status_code=404,
            detail="Image not found",
        )

    return (
        db.query(AICallLog)
        .filter(AICallLog.image_id == image_id)
        .order_by(AICallLog.created_at.desc())
        .all()
    )