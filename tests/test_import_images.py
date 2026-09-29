from scripts.import_images import ALLOWED_EXTENSIONS


def test_allowed_image_extensions():
    assert ".jpg" in ALLOWED_EXTENSIONS
    assert ".jpeg" in ALLOWED_EXTENSIONS
    assert ".png" in ALLOWED_EXTENSIONS
    assert ".webp" in ALLOWED_EXTENSIONS