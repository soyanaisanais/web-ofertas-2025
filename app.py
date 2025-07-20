from flask import Flask, render_template, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Conexión a MongoDB (usa tus credenciales)
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
            datos = list(coleccion.find({}).sort("fecha", -1).limit(6))
        elif categoria == "electronica":
            datos = list(coleccion.find({"categoria": "Electronics"}).sort("fecha", -1).limit(6))
        elif categoria == "deportes":
            datos = list(coleccion.find({"categoria": "Sports"}).sort("fecha", -1).limit(6))
        else:
            return jsonify({"error": "Categoría no válida"}), 400

        if not datos:
            return jsonify({"error": "No hay ofertas"}), 404

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
