from flask import Flask, render_template, jsonify
import os
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

# Configuración de MongoDB
MONGO_URI = os.getenv("MONGO_URI") or "mongodb+srv://soyanaisanais:Eduardo1981@cluster0.yaamkjc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "Chollos_2025"
COLLECTION_NAME = "Ultimas_Ofertas"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# 🔁 Solo una vez: convierte 'img' en 'imagen'
if collection.count_documents({"img": {"$exists": True}}) > 0:
    collection.update_many(
        {"img": {"$exists": True}},
        [{"$set": {"imagen": "$img"}}, {"$unset": "img"}]
    )

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

