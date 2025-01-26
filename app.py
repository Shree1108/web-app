from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader, PdfWriter
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    uploaded_files = request.files.getlist('pdf_files')
    output_file_path = os.path.join(OUTPUT_FOLDER, 'merged.pdf')

    if len(uploaded_files) < 2:
        return "Please upload at least two PDF files to merge."

    try:
        writer = PdfWriter()
        for file in uploaded_files:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            reader = PdfReader(file_path)
            for page in reader.pages:
                writer.add_page(page)

        with open(output_file_path, "wb") as output_file:
            writer.write(output_file)

        return send_file(output_file_path, as_attachment=True)
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/extract', methods=['POST'])
def extract_pages():
    uploaded_file = request.files['pdf_file']
    page_range = request.form.get('page_range')
    output_file_path = os.path.join(OUTPUT_FOLDER, 'extracted.pdf')

    if not uploaded_file or not page_range:
        return "Please upload a PDF file and specify the page range."

    try:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)

        start, end = map(int, page_range.split('-'))
        reader = PdfReader(file_path)
        writer = PdfWriter()

        for page_number in range(start - 1, end):
            writer.add_page(reader.pages[page_number])

        with open(output_file_path, "wb") as output_file:
            writer.write(output_file)

        return send_file(output_file_path, as_attachment=True)
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
