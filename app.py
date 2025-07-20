from flask import Flask, render_template, jsonify
import os
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

# Carga variables de entorno para MongoDB
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DATABASE_NAME", "Chollos_2025")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "Ultimas_Ofertas")

# Conexión a MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/general')
def get_general():
    data = []
    for doc in collection.find().sort("fecha", -1).limit(12):
        data.append({
            "titulo": doc.get("titulo", doc.get("categoria", "Oferta")),
            "imagen": doc.get("imagen", ""),
            "precio": doc.get("precio", ""),
            "descuento": doc.get("descuento", 0),
            "url": doc.get("url", "")
        })
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
