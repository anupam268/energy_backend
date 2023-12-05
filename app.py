
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app,resources={r"/process_data": {"origins": "http://localhost:3000"}}, methods=["POST", "GET"])

data_storage = 'data.json'

def store_data(data):
    with open(data_storage, 'w') as f:
        json.dump(data, f)

def retrieve_data():
    try:
        with open(data_storage, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return None

def categorize_energy(data):
    renewable_categories = ['wind generation', 'solar generation', 'hydro generation']
    traditional_categories = ['coal generation', 'ignite gas, naphtha, diesel generation', 'nuclear generation']

    renewable_energy = []
    traditional_energy = []

    # If data is a dictionary, treat it as a single entry
    if isinstance(data, dict):
        category = data.get('category', '').lower()
        if category in renewable_categories:
            renewable_energy.append(data)
        elif category in traditional_categories:
            traditional_energy.append(data)
    elif isinstance(data, list):
        # If data is a list, iterate over each entry
        for entry in data:
            category = entry.get('category', '').lower()
            if category in renewable_categories:
                renewable_energy.append(entry)
            elif category in traditional_categories:
                traditional_energy.append(entry)

    return {
        'renewable_energy': renewable_energy,
        'traditional_energy': traditional_energy
    }


@app.route('/process_data', methods=['GET', 'POST'])
def process_data():
    if request.method == 'GET':
        headers = {
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Methods': 'POST, OPTIONS, GET',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return jsonify({'message': 'This is a GET request'}), 200, headers

    try:
        data = request.get_json()
        print("Received data:", data)
        if not data:
            # If data is empty or not in JSON format, consider it as an empty dictionary
            data = {}

        # Store data
        store_data(data)

        # Categorize data
        categorized_data = categorize_energy(data)

        return jsonify(categorized_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
