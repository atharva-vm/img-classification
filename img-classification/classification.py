from pathlib import Path


def classify_image(filename):
    """
    Classify an uploaded image by its file extension.

    Returns:
        "PNG" for .png files
        "JPG" for .jpg and .jpeg files
        None for unsupported file types
    """
    extension = Path(filename).suffix.lower()

    if extension == ".png":
        return "PNG"

    if extension in {".jpg", ".jpeg"}:
        return "JPG"

    return None
