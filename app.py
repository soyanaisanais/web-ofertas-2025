from flask import Flask, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# Conexión a MongoDB (tus credenciales)
MONGO_URI = "mongodb+srv://soyanaisanais:Eduardo1981@cluster0.yaamkjc.mongodb.net/Chollos_2025?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["Chollos_2025"]

@app.route('/api/<categoria>')
def api(categoria):
    try:
        # Define qué colección usar para cada categoría
        colecciones = {
            "general": db["Ultimas_Ofertas"],
            "electronica": db["publicados_electronica"],
            "deportes": db["publicados_deports"]
        }
        
        # Obtener 6 ofertas más recientes
        datos = list(colecciones[categoria].find().sort("fecha", -1).limit(6))
        
        if not datos:
            return jsonify({"error": "No hay ofertas disponibles"}), 404

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
