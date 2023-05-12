"""
Dependencies
pip install -U Flask
pip install -U flask_cors
pip install QuantConnect


Test
http://127.0.0.1:5000/
"""

from flask import Flask, jsonify, request
from flask_cors.extension import CORS
from controller import ChartsController
import os

app = Flask(__name__)

# Define CORS
CORS(app, origins=[
    "http://localhost:6006",
    "http://127.0.0.1:5173",
    "http://localhost:3000"
])
app.config['CORS HEADERS'] = 'Content-Type'

# Instanciate controller
controller = ChartsController()

@app.route('/api/analysis', methods=['POST'])
def analysis():
    data = request.get_json()
    data = controller.analyze(data)
    return jsonify(data)

@app.route('/api/normalize', methods=['POST'])
def normalize():
    data = request.get_json()
    data = controller.normalize_data(data)
    controller.clear()
    return jsonify(data)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

