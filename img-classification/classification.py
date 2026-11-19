import uuid
from pathlib import Path

from PIL import Image, UnidentifiedImageError
from werkzeug.utils import secure_filename

from database import save_image_record

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def classify_image(filename):
    """Return PNG, JPG, or None based on the filename extension."""
    extension = Path(filename).suffix.lower()
    if extension == ".png":
        return "PNG"
    if extension in {".jpg", ".jpeg"}:
        return "JPG"
    return None


def validate_image(stream):
    """Validate actual image content and return category, format and dimensions."""
    stream.seek(0)
    with Image.open(stream) as image:
        detected_format = image.format
        if detected_format not in {"PNG", "JPEG"}:
            raise UnidentifiedImageError("Unsupported image format")
        image.verify()

    stream.seek(0)
    with Image.open(stream) as image:
        width, height = image.size

    category = "PNG" if detected_format == "PNG" else "JPG"
    return category, detected_format, width, height


def process_uploaded_image(image, image_dir, base_dir):
    """Validate, classify, save the image and record its metadata in MySQL."""
    if not image or not image.filename:
        raise ValueError("No file selected.")

    original_name = secure_filename(image.filename)
    if not original_name:
        raise ValueError("Invalid filename.")

    extension_category = classify_image(original_name)
    if extension_category is None:
        raise ValueError("Only PNG and JPG/JPEG images are allowed.")

    try:
        category, detected_format, width, height = validate_image(image.stream)
    except (UnidentifiedImageError, OSError, ValueError) as error:
        raise ValueError("The uploaded file is not a valid PNG or JPG image.") from error

    if category != extension_category:
        raise ValueError("The file extension does not match the actual image format.")

    image.stream.seek(0)
    destination_folder = Path(image_dir) / category
    destination_folder.mkdir(parents=True, exist_ok=True)

    stored_name = f"{uuid.uuid4().hex}{Path(original_name).suffix.lower()}"
    destination = destination_folder / stored_name
    relative_path = destination.relative_to(Path(base_dir)).as_posix()

    try:
        image.save(destination)
        save_image_record(
            original_name, stored_name, category, relative_path,
            destination.stat().st_size
        )
    except Exception:
        destination.unlink(missing_ok=True)
        raise

    return {
        "filename": original_name,
        "category": category,
        "saved_to": relative_path,
        "width": width,
        "height": height,
    }
