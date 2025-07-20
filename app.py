from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# Conexión a MongoDB (usa TUS claves directamente)
MONGO_URI = "mongodb+srv://soyanaisanais:Eduardo1981@cluster0.yaamkjc.mongodb.net/Chollos_2025?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["Chollos_2025"]
coleccion = db["Ultimas_Ofertas"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/<categoria>')
def api(categoria):
    try:
        if categoria == "general":
            filtro = {}
        elif categoria == "electronica":
            filtro = {"categoria": "Electronics"}
        elif categoria == "deportes":
            filtro = {"categoria": "Sports"}
        else:
            return jsonify({"error": "Categoría no válida"}), 400

        datos = list(coleccion.find(filtro).sort("fecha", -1).limit(10))
        return jsonify([{
            "imagen": d.get("imagen", ""),
            "titulo": d.get("titulo", "Sin título"),
            "precio": d.get("precio", "?"),
            "descuento": d.get("descuento", 0),
            "url": d.get("url", "#")
        } for d in datos])
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
