from flask import Flask, request, jsonify
from shared.file_util import get_file_crc32
import pandas as pd
import json
import os

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_excel_to_json():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        crc32_checksum = get_file_crc32(file)
        file.seek(0)  # Reset file pointer to the beginning
        df = pd.read_excel(file)
        result = df.to_json(orient='records')

         # Ensure the data directory exists
        os.makedirs('./data', exist_ok=True)

       # Check if the JSON file with the CRC32 name already exists
        json_filename = f'./data/{crc32_checksum}.json'
        if os.path.exists(json_filename):
            return jsonify({"error": "Arquivo já processado"}), 400

        # Save the JSON file with the name as the CRC32 value
        with open(json_filename, 'w') as json_file:
            json.dump(json.loads(result), json_file, indent=4)

        return jsonify({"crc32": crc32_checksum, "data": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)