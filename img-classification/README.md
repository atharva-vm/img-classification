# Image Classification (Flask + MySQL)

Upload PNG/JPG/JPEG images through the browser. The application checks the actual image content, stores the file in its matching folder, records upload details in MySQL, and displays live database counts and the 10 most recent uploads.

## Features

- PNG files are saved under `Images/PNG/`.
- JPG/JPEG files are saved under `Images/JPG/`.
- Validates real image format (a renamed or fake file is rejected).
- 10 MB upload limit.
- UUID-based stored filenames prevent accidental overwrites.
- MySQL stores original name, stored name, category, relative path, file size, and upload time.
- Dashboard shows total, PNG, and JPG counts plus recent uploads.
- Drag-and-drop, image preview, and responsive layout.
- If the database insert fails, the newly saved file is removed to avoid an untracked upload.

## 1. Create the MySQL database

Run this once in MySQL Workbench or the MySQL command line:

```sql
CREATE DATABASE image_classification
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

The application creates the `image_uploads` table automatically at startup. The MySQL user needs permission to create tables and read/insert rows in this database.

## 2. Install Python dependencies

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Then:
```bash
python -m pip install -r requirements.txt
```

## 3. Configure database credentials

Set environment variables before starting the app. Defaults are `localhost`, port `3306`, user `root`, empty password, and database `image_classification`.

Windows PowerShell:
```powershell
$env:DB_HOST="localhost"
$env:DB_PORT="3306"
$env:DB_USER="root"
$env:DB_PASSWORD="your_mysql_password"
$env:DB_NAME="image_classification"
```

macOS/Linux:
```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD='your_mysql_password'
export DB_NAME=image_classification
```

## 4. Run

```bash
python app.py
```

Open http://127.0.0.1:5000.

## Database count query

```sql
SELECT
    COUNT(*) AS total_images,
    SUM(category = 'PNG') AS png_images,
    SUM(category = 'JPG') AS jpg_images
FROM image_uploads;
```

## Project structure

```text
img-classification/
├── app.py
├── classification.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── Images/
    ├── PNG/
    └── JPG/
```

Note: MySQL Server must be installed and running separately. Do not commit real database passwords to source control; use environment variables.


## Updated code separation

- `app.py`: Flask routes and request/response handling only.
- `classification.py`: image validation, classification and file-saving logic.
- `database.py`: MySQL connection, SELECT queries, INSERT query and statistics.
- `create_table.sql`: run this SQL separately in MySQL Workbench before launching the app.

The app no longer creates the table automatically.
