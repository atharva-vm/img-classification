# img-classification

A small Flask application that accepts PNG and JPG/JPEG uploads and saves each image into the matching folder.

## Project structure

```text
img-classification/
├── app.py
├── classification.py
├── requirements.txt
├── templates/
│   └── index.html
└── Images/
    ├── PNG/
    └── JPG/
```

## Run locally

1. Open a terminal in this project folder.
2. (Recommended) Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the Flask app:

   ```bash
   python app.py
   ```

5. Open http://127.0.0.1:5000 in your browser.

Uploaded `.png` files are saved in `Images/PNG`; `.jpg` and `.jpeg` files are saved in `Images/JPG`. Maximum upload size is 10 MB.
