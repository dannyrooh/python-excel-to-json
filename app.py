from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_excel_to_json():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        df = pd.read_excel(file)
        result = df.to_json(orient='records')
        return result, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)