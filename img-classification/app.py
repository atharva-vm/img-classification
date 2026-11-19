from pathlib import Path

import pymysql
from flask import Flask, jsonify, render_template, request

from classification import process_uploaded_image
from database import get_statistics, get_db_connection

BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "Images"

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB per image


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/stats", methods=["GET"])
def api_stats():
    try:
        counts, recent = get_statistics()
        return jsonify({"success": True, "counts": counts, "recent": recent})
    except pymysql.MySQLError:
        app.logger.exception("Unable to read image statistics from MySQL")
        return jsonify({
            "success": False,
            "message": "Database is unavailable. Check your MySQL settings."
        }), 503


@app.route("/api/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"success": False, "message": "Please select an image."}), 400

    try:
        result = process_uploaded_image(request.files["image"], IMAGE_DIR, BASE_DIR)
        counts, _recent = get_statistics()
        return jsonify({
            "success": True,
            "message": "Image uploaded and saved successfully.",
            **result,
            "counts": counts
        }), 201
    except ValueError as error:
        return jsonify({"success": False, "message": str(error)}), 400
    except pymysql.MySQLError:
        app.logger.exception("Upload could not be recorded in MySQL")
        return jsonify({
            "success": False,
            "message": "Upload could not be recorded. Check the MySQL connection and try again."
        }), 503
    except OSError:
        app.logger.exception("Image file could not be saved")
        return jsonify({
            "success": False,
            "message": "Image could not be saved. Please try again."
        }), 500


@app.errorhandler(413)
def file_too_large(_error):
    return jsonify({"success": False, "message": "Image must be 10 MB or smaller."}), 413


if __name__ == "__main__":
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    try:
        # Table is created separately using create_table.sql.
        connection = get_db_connection()
        connection.close()
        print("MySQL connected successfully.")
    except pymysql.MySQLError as error:
        raise SystemExit(
            f"MySQL connection failed: {error}\n"
            "Check DB_HOST, DB_USER, DB_PASSWORD and DB_NAME."
        )

    app.run(host="127.0.0.1", port=5000, debug=False)
