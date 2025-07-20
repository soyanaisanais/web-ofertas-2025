from flask import Flask, jsonify, render_template, send_from_directory
from pymongo import MongoClient
import os

app = Flask(__name__, static_folder='static')

# Conexión a MongoDB (TUS DATOS ORIGINALES)
MONGO_URI = "mongodb+srv://soyanaisanais:Eduardo1981@cluster0.yaamkjc.mongodb.net/Chollos_2025?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI, connectTimeoutMS=30000, socketTimeoutMS=30000)
db = client["Chollos_2025"]

# Ruta para el QR
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/general')
def general():
    try:
        ofertas = list(db["Ultimas_Ofertas"].find().sort("fecha", -1).limit(6))
        return jsonify([{
            "_id": str(o["_id"]),
            "titulo": o.get("titulo", "Oferta especial"),
            "precio": o.get("precio", "Consultar"),
            "descuento": o.get("descuento", 0),
            "url": o.get("url", "#"),
            "imagen": o.get("imagen", "").replace("http://", "https://") or "https://via.placeholder.com/300x200?text=Chollo+2025"
        } for o in ofertas])
    except Exception as e:
        return jsonify({"error": "Error cargando ofertas"}), 500

@app.route('/api/electronica')
def electronica():
    try:
        ofertas = list(db["publicados_electronica"].find().sort("fecha", -1).limit(6))
        return jsonify([{
            "_id": str(o["_id"]),
            "titulo": o.get("titulo", "Electrónica"),
            "precio": o.get("precio", "Consultar"),
            "descuento": o.get("descuento", 0),
            "url": o.get("url", "#"),
            "imagen": o.get("imagen", "").replace("http://", "https://") or "https://via.placeholder.com/300x200?text=Electrónica"
        } for o in ofertas])
    except Exception as e:
        return jsonify({"error": "Error cargando electrónica"}), 500

@app.route('/api/deportes')
def deportes():
    try:
        ofertas = list(db["publicados_deportes"].find().sort("fecha", -1).limit(6))
        return jsonify([{
            "_id": str(o["_id"]),
            "titulo": o.get("titulo", "Deportes"),
            "precio": o.get("precio", "Consultar"),
            "descuento": o.get("descuento", 0),
            "url": o.get("url", "#"),
            "imagen": o.get("imagen", "").replace("http://", "https://") or "https://via.placeholder.com/300x200?text=Deportes"
        } for o in ofertas])
    except Exception as e:
        return jsonify({"error": "Error cargando deportes"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
