
from flask import Flask, request, render_template, send_file, send_from_directory, abort
import os
from PIL import Image
from werkzeug.utils import secure_filename
import uuid
import time

app = Flask(__name__)
UPLOAD_FOLDER = os.path.abspath('uploads')
CONVERTED_FOLDER = os.path.abspath('converted')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

# Limit uploads to 16 MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Allowed extensions for upload/conversion
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf'}


def image_to_pdf(image_path, pdf_path):
	image = Image.open(image_path)
	if image.mode == "RGBA":
		image = image.convert("RGB")
	image.save(pdf_path, "PDF", resolution=100.0)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	converted_filename = None
	error = None
	if request.method == 'POST':
		file = request.files.get('file')
		target_format = request.form.get('format')

		if not file or file.filename == '':
			error = 'No file provided.'
			return render_template('index.html', converted_filename=None, error=error)

		filename = secure_filename(file.filename)
		if '.' in filename:
			ext = filename.rsplit('.', 1)[1].lower()
		else:
			ext = ''

		if ext not in ALLOWED_EXTENSIONS:
			error = f'File extension .{ext} is not allowed.'
			return render_template('index.html', converted_filename=None, error=error)

		# make filename unique to avoid collisions
		unique_suffix = uuid.uuid4().hex
		name_root = os.path.splitext(filename)[0]
		filename_unique = f"{name_root}_{unique_suffix}.{ext}"
		filepath = os.path.join(UPLOAD_FOLDER, filename_unique)
		file.save(filepath)

		# Conversion logic
		try:
			if target_format == 'pdf' and ext in ('jpg', 'jpeg', 'png'):
				converted_filename = os.path.splitext(filename_unique)[0] + '.pdf'
				converted_path = os.path.join(CONVERTED_FOLDER, converted_filename)
				image_to_pdf(filepath, converted_path)
			else:
				# For now, copy the file to converted directory
				converted_filename = filename_unique
				converted_path = os.path.join(CONVERTED_FOLDER, converted_filename)
				with open(filepath, 'rb') as src, open(converted_path, 'wb') as dst:
					dst.write(src.read())
		except Exception as e:
			error = f'Conversion failed: {e}'
			converted_filename = None
		finally:
			# remove the uploaded file; we don't need to keep original uploads
			try:
				if os.path.exists(filepath):
					os.remove(filepath)
			except Exception:
				pass

	return render_template('index.html', converted_filename=converted_filename, error=error)

@app.route('/download/<filename>')
def download_file(filename):
	# sanitize filename before serving
	safe_name = secure_filename(filename)
	filepath = os.path.join(CONVERTED_FOLDER, safe_name)
	if not os.path.exists(filepath):
		abort(404)
	return send_from_directory(CONVERTED_FOLDER, safe_name, as_attachment=True)

if __name__ == '__main__':
	app.run(debug=False)
