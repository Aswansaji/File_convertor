# File_convertor

Simple Flask-based file converter that accepts image uploads (JPG/PNG) and converts them to PDF. The app now includes a modern Bootstrap UI, safer upload handling, file validation, and automatic removal of uploaded source files after conversion.

## Features
- Upload images via drag-and-drop or file picker
- Convert images to PDF (or keep original formats)
- Safe filename handling and allowed-extension checks
- Limits upload size to 16 MB
- Uploaded source files are deleted after conversion

## Requirements
- Python 3.10+
- pip
- The project uses these Python packages: `Flask`, `Pillow` (PIL), `requests` (for tests)

## Setup
1. (Optional) Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

If `requirements.txt` is not present, install manually:

```powershell
pip install flask pillow requests
```

## Run the app

```powershell
python main.py
```

Then open http://127.0.0.1:5000 in your browser.

## Testing locally (automated)
A small test script `upload_test.py` is included which creates a sample image and POSTs it to the running server. Run it while the server is running:

```powershell
python upload_test.py
```

You can also run tests using Flask's test client without starting the server:

```powershell
python run_test_client.py
```

## Notes
- The app runs with the Flask development server. Use a production WSGI server (gunicorn/uWSGI) for deployment.
- Converted files are stored in the `converted/` directory. Uploaded source files are removed after conversion.
- Adjust `ALLOWED_EXTENSIONS` and `MAX_CONTENT_LENGTH` in `main.py` as needed.

## Contributing
Create a branch, commit your changes, and open a pull request.

---
Generated and updated by project maintainer.
