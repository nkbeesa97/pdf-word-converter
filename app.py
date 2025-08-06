from flask import Flask, request, send_file
import os
import pypandoc
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "/tmp"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400

    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400

    target_format = request.form.get('target_format')
    if not target_format:
        return {'error': 'No target format specified'}, 400

    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(input_path)

    output_filename = f"converted.{target_format}"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

    try:
        pypandoc.convert_file(input_path, target_format, outputfile=output_path)
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
