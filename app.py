from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# MongoDB Atlas
mongo_uri = "mongodb+srv://soyanaisanais:Eduardo1981@cluster0.z8p2p0v.mongodb.net/?retryWrites=true&w=majority"
cliente = MongoClient(mongo_uri)
db = cliente["amazon"]

@app.route("/api/chollos")
def chollos():
    datos = db["publicados"].find().sort("fecha", -1).limit(4)
    return jsonify([normalizar(doc) for doc in datos])

@app.route("/api/electronica")
def electronica():
    datos = db["publicados_electronica"].find().sort("fecha", -1).limit(4)
    return jsonify([normalizar(doc) for doc in datos])

@app.route("/api/deportes")
def deportes():
    datos = db["publicados_deportes"].find().sort("fecha", -1).limit(4)
    return jsonify([normalizar(doc) for doc in datos])

def normalizar(doc):
    return {
        "titulo": doc.get("titulo", ""),
        "precio": doc.get("precio", ""),
        "descuento": doc.get("descuento", 0),
        "url": doc.get("url", ""),
        "img": doc.get("img", ""),
        "fecha": doc.get("fecha", datetime.now()).isoformat()
    }

if __name__ == "__main__":
    app.run(debug=True, port=5000)
