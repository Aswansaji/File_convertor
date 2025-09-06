
from flask import Flask, request, render_template, send_file
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)


def image_to_pdf(image_path, pdf_path):
	image = Image.open(image_path)
	if image.mode == "RGBA":
		image = image.convert("RGB")
	image.save(pdf_path, "PDF", resolution=100.0)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	converted_filename = None
	if request.method == 'POST':
		file = request.files['file']
		target_format = request.form['format']
		if file:
			filename = file.filename
			filepath = os.path.join(UPLOAD_FOLDER, filename)
			file.save(filepath)
			# Conversion logic
			if target_format == 'pdf' and filename.lower().endswith(('jpg', 'jpeg', 'png')):
				converted_filename = os.path.splitext(filename)[0] + '.pdf'
				converted_path = os.path.join(CONVERTED_FOLDER, converted_filename)
				image_to_pdf(filepath, converted_path)
			else:
				# For now, just copy the file as 'converted'
				converted_filename = filename
				converted_path = os.path.join(CONVERTED_FOLDER, converted_filename)
				with open(filepath, 'rb') as src, open(converted_path, 'wb') as dst:
					dst.write(src.read())
	return render_template('index.html', converted_filename=converted_filename)

@app.route('/download/<filename>')
def download_file(filename):
	filepath = os.path.join(CONVERTED_FOLDER, filename)
	return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
	app.run(debug=True)
