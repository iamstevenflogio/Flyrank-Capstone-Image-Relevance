from datetime import datetime 
from typing import Any

from pydantic import BaseModel, ConfigDict

class ImageMetadataResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    subject: str
    category: str
    attributes: Any
    caption: str
    confidence: float 
    model_name: str
    created_at: datetime 

class ImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    file_path: str
    status: str
    attempts: int
    error_message: str | None
    created_at: datetime
    metadata_record: ImageMetadataResponse | None

class AICallLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_id: int
    provider: str
    model_name: str
    status: str
    input_tokens: int | None
    output_tokens: int | None
    estimated_cost_usd: float
    error_message: str | None
    created_at: datetime