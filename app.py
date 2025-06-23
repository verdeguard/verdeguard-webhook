from flask import Flask, request, jsonify
import requests
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Roboflow API settings
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

        # Fetch image bytes from URL
        response = requests.get(image_url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to download image"}), 400

        # Convert image to base64
        image_base64 = base64.b64encode(response.content).decode("utf-8")

        # Send to Roboflow using base64 format
        roboflow_response = requests.post(
            f"https://detect.roboflow.com/{ROBOFLOW_MODEL}/{ROBOFLOW_VERSION}?api_key={ROBOFLOW_API_KEY}",
            json={"image": image_base64},
            headers={"Content-Type": "application/json"}
        )

        return jsonify(roboflow_response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

