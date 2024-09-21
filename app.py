from flask import Flask, request, render_template, send_file
from pdf2docx import Converter
import os
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf_file' not in request.files:
        return "No file uploaded", 400
    
    pdf_file = request.files['pdf_file']
    
    if pdf_file.filename == '':
        return "No selected file", 400
    
    pdf_file_path = os.path.join('uploads', pdf_file.filename)
    pdf_file.save(pdf_file_path)

    docx_file_path = pdf_file_path.replace('.pdf', '.docx')

    start_time = time.time()  # Track the conversion time

    try:
        # Create a Converter object
        cv = Converter(pdf_file_path)
        
        # Convert PDF to DOCX
        cv.convert(docx_file_path)  # Convert the entire document in one go
        cv.close()

        conversion_time = time.time() - start_time
        print(f"Conversion completed in {conversion_time:.2f} seconds.")

        # Inform the user about the time taken
        return send_file(docx_file_path, as_attachment=True), {'X-Conversion-Time': f"{conversion_time:.2f} seconds"}
    except Exception as e:
        print(f"Error during conversion: {e}")
        return f"Error during conversion: {e}", 500

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
