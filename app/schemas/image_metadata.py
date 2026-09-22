from pydantic import BaseModel, Field, field_validator


class ImageMetadata(BaseModel):
    subject: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=100)
    attributes: list[str] = Field(min_length=1, max_length=10)
    caption: str = Field(min_length=5, max_length=500)
    confidence: float = Field(ge=0.0, le=1.0)

    @field_validator("subject", "category", "caption")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        return value.strip().lower()

    @field_validator("attributes")
    @classmethod
    def normalize_attributes(cls, values: list[str]) -> list[str]:
        cleaned = [value.strip().lower() for value in values if value.strip()]

        if not cleaned:
            raise ValueError("attributes must contain at least one non-empty value")

        return cleaned