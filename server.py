from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load the CSV data
def load_csv_data():
    try:
        data = pd.read_csv('dwlr_data.csv')
        data['Date'] = pd.to_datetime(data['Date'])
        return data
    except Exception as e:
        return str(e)

# Simple z-score anomaly detection
def detect_anomalies(data):
    data['ZScore'] = (data['GW Level(mbgl)'] - data['GW Level(mbgl)'].mean()) / data['GW Level(mbgl)'].std()
    anomalies = data[data['ZScore'].abs() > 2]  # Z-score threshold of 2
    return anomalies

@app.route('/data', methods=['GET'])
def get_data():
    # Load data
    data = load_csv_data()
    if isinstance(data, str):  # If error occurred
        return jsonify({'error': data})

    # Detect anomalies
    anomalies = detect_anomalies(data)

    # Get the latest record
    latest_record = data.iloc[-1]

    # Convert data to JSON
    response = {
        'timestamps': data['Date'].dt.strftime('%Y-%m-%d').tolist(),
        'telemetry': data['GW Level(mbgl)'].tolist(),
        'anomalies': anomalies['Date'].dt.strftime('%Y-%m-%d').tolist(),
        'location': latest_record['Station Name'],
        'agency': latest_record['Agency Name'],
        'basin': latest_record['Basin'],
        'subbasin': latest_record['Subbasin'],
        'stationType': latest_record['Station Type']
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)