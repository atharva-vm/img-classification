import os
import pymysql

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "image_classification"),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "connect_timeout": 5,
    "autocommit": True,
}


def get_db_connection():
    """Create and return a MySQL database connection."""
    return pymysql.connect(**DB_CONFIG)


def get_statistics():
    """Fetch total, PNG and JPG counts and the latest 10 uploads."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) AS total,
                       COALESCE(SUM(category = 'PNG'), 0) AS png_count,
                       COALESCE(SUM(category = 'JPG'), 0) AS jpg_count
                FROM image_uploads
            """)
            counts = cursor.fetchone()

            cursor.execute("""
                SELECT id, original_filename, stored_filename, category,
                       file_size, uploaded_at
                FROM image_uploads
                ORDER BY uploaded_at DESC, id DESC
                LIMIT 10
            """)
            recent = cursor.fetchall()

            for item in recent:
                if item["uploaded_at"]:
                    item["uploaded_at"] = item["uploaded_at"].strftime("%Y-%m-%d %H:%M:%S")

        return counts, recent
    finally:
        connection.close()


def save_image_record(original_name, stored_name, category, relative_path, file_size):
    """Insert image metadata into MySQL."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO image_uploads
                    (original_filename, stored_filename, category, file_path, file_size)
                VALUES (%s, %s, %s, %s, %s)
            """, (original_name, stored_name, category, relative_path, file_size))
        connection.commit()
    finally:
        connection.close()
