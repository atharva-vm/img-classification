from pathlib import Path
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from classification import classify_image

BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "Images"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB per image


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"success": False, "message": "Please select an image."}), 400

    image = request.files["image"]

    if not image.filename:
        return jsonify({"success": False, "message": "No file selected."}), 400

    category = classify_image(image.filename)
    if category is None:
        return jsonify({
            "success": False,
            "message": "Only PNG and JPG/JPEG images are allowed."
        }), 400

    safe_filename = secure_filename(image.filename)
    destination_folder = IMAGE_DIR / category
    destination_folder.mkdir(parents=True, exist_ok=True)

    destination = destination_folder / safe_filename

    # Avoid overwriting an existing file with the same name.
    counter = 1
    while destination.exists():
        stem = Path(safe_filename).stem
        suffix = Path(safe_filename).suffix
        destination = destination_folder / f"{stem}_{counter}{suffix}"
        counter += 1

    image.save(destination)

    return jsonify({
        "success": True,
        "message": "Image uploaded successfully.",
        "filename": destination.name,
        "category": category,
        "saved_to": str(destination.relative_to(BASE_DIR))
    })


@app.errorhandler(413)
def file_too_large(_error):
    return jsonify({"success": False, "message": "Image must be 10 MB or smaller."}), 413


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
