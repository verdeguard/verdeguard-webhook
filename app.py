from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Roboflow API
ROBOFLOW_API_KEY = "mkjvwtXSGUYXP95Ob8cu"
ROBOFLOW_MODEL = "verdeguard-plant-classifier"
ROBOFLOW_VERSION = "1"

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "VerdeGuard webhook is live!"})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        image_url = data.get("url")

        if not image_url:
            return jsonify({"error": "No image URL provided"}), 400

        endpoint = f"https://detect.roboflow.com/{ROBOFLOW_MODEL}/{ROBOFLOW_VERSION}?api_key={ROBOFLOW_API_KEY}"
        response = requests.post(
            endpoint,
            json={"url": image_url},
            headers={"Content-Type": "application/json"}
        )

        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
