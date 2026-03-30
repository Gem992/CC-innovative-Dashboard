"""
Edge Server – Agent 1
Lightweight Flask server exposing POST /edge/send
Applies the edge filter and forwards anomalies to the cloud backend.
"""

import sys
import os
import time
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# Ensure edge/ dir is on path so edge_filter is importable from any cwd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edge_filter import filter_reading

app = Flask(__name__)
CORS(app)

CLOUD_URL = "http://localhost:8000/data"   # Cloud FastAPI endpoint


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "edge-server"}), 200


@app.route("/edge/send", methods=["POST"])
def receive_reading():
    """
    Accept a sensor reading, apply edge filtering,
    and forward anomalies to the cloud API.
    """
    reading = request.get_json(force=True)

    if not reading:
        return jsonify({"error": "Empty payload"}), 400

    edge_start = time.time()
    result = filter_reading(reading)
    edge_latency_ms = round((time.time() - edge_start) * 1000, 2)

    response_payload = {
        "forwarded": False,
        "reason": result["reason"],
        "edge_latency_ms": edge_latency_ms,
        "reading": reading,
    }

    if result["forward"]:
        cloud_start = time.time()
        try:
            cloud_resp = requests.post(
                CLOUD_URL,
                json={**reading, "edge_latency_ms": edge_latency_ms},
                timeout=10,
            )
            cloud_latency_ms = round((time.time() - cloud_start) * 1000, 2)
            response_payload.update(
                {
                    "forwarded": True,
                    "cloud_status": cloud_resp.status_code,
                    "cloud_latency_ms": cloud_latency_ms,
                    "cloud_response": cloud_resp.json() if cloud_resp.ok else {},
                }
            )
        except requests.exceptions.ConnectionError:
            response_payload["cloud_error"] = "Cloud backend not reachable"

    return jsonify(response_payload), 200


if __name__ == "__main__":
    print("🌐 Edge Server running on http://localhost:5001")
    app.run(host="0.0.0.0", port=5001, debug=False)
