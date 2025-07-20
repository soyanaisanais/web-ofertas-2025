from flask import Flask, jsonify, render_template, send_from_directory
from pymongo import MongoClient
from bson.json_util import dumps
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Conexión MongoDB
MONGO_URI = "mongodb+srv://soyanaisanais:Eduardo1981@cluster0.yaamkjc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["Chollos_2025"]
collection = db["Ultimas_Ofertas"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

@app.route("/api/general")
def api_general():
    try:
        docs = list(collection.find().sort("fecha", -1).limit(10))
        return dumps(docs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/electronica")
def api_electronica():
    try:
        docs = list(collection.find({"categoria": "Electronics"}).sort("fecha", -1).limit(10))
        return dumps(docs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/deportes")
def api_deportes():
    try:
        docs = list(collection.find({"categoria": "Sports"}).sort("fecha", -1).limit(10))
        return dumps(docs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
