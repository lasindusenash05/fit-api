from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Optional: allows requests from browsers

# Get MongoDB URI from environment variable
MONGO_URI = os.environ.get("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["fitness_db"]
collection = db["reports"]

# Root route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Fitness API is running."})

# Add new fitness report
@app.route("/report", methods=["POST"])
def add_report():
    data = request.json
    today = datetime.now().strftime("%Y-%m-%d")
    report = {
        "date": today,
        "message": data.get("message", "No message provided.")
    }
    collection.insert_one(report)
    return jsonify({"status": "success", "data": report}), 201

# Get all reports
@app.route("/report", methods=["GET"])
def get_reports():
    reports = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB _id field
    return jsonify({"reports": reports})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
