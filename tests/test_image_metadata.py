import pytest
from pydantic import ValidationError

from app.schemas.image_metadata import ImageMetadata


def test_valid_image_metadata():
    metadata = ImageMetadata(
        subject="Red Fox",
        category="Animal",
        attributes=["Orange Fur", "Forest", "Wild"],
        caption="A red fox standing in a green forest.",
        confidence=0.94,
    )

    assert metadata.subject == "red fox"
    assert metadata.category == "animal"
    assert metadata.attributes == ["orange fur", "forest", "wild"]
    assert metadata.confidence == 0.94


def test_rejects_invalid_confidence():
    with pytest.raises(ValidationError):
        ImageMetadata(
            subject="wolf",
            category="animal",
            attributes=["forest"],
            caption="A wolf standing in a forest.",
            confidence=1.5,
        )


def test_rejects_empty_attributes():
    with pytest.raises(ValidationError):
        ImageMetadata(
            subject="wolf",
            category="animal",
            attributes=[],
            caption="A wolf is standing in a forest.",
            confidence=0.91,
        )