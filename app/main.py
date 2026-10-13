from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import SessionLocal
from app.models.image import Image
from app.schemas.image_response import ImageResponse

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
def list_images(db: Session = Depends(get_db)):
    return (
        db.query(Image)
        .options(joinedload(Image.metadata_record))
        .order_by(Image.id)
        .all()
    )

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