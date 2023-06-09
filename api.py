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
    "http://localhost:3000",
    "https://market-tools-27f02.web.app"
])
app.config['CORS HEADERS'] = 'Content-Type'

# Instanciate controller
controller = ChartsController()

@app.route('/api/analysis', methods=['POST', 'GET'])
def analysis():

    try:
        data = request.get_json()
        data = controller.analyze(data)
        return jsonify(data)
    except:
        return jsonify(-1)

@app.route('/api/available', methods=['GET'])
def available():
    return jsonify(True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv("PORT", default=5000))
