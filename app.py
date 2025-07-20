from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# Conexión a MongoDB (tus credenciales ya integradas)
MONGO_URI = "mongodb+srv://soyanaisanais:Eduardo1981@cluster0.yaamkjc.mongodb.net/Chollos_2025?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["Chollos_2025"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/general')
def general():
    try:
        datos = list(db["Ultimas_Ofertas"].find().sort("fecha", -1).limit(6))
        return jsonify([{
            "titulo": d.get("titulo", "Sin título"),
            "precio": d.get("precio", "?"),
            "descuento": d.get("descuento", 0),
            "url": d.get("url", "#"),
            "imagen": d.get("imagen", "/static/placeholder.jpg"),
            "fecha": str(d.get("fecha", ""))
        } for d in datos])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/electronica')
def electronica():
    try:
        datos = list(db["publicados_electronica"].find().sort("fecha", -1).limit(6))
        return jsonify([{
            "titulo": d.get("titulo", "Sin título"),
            "precio": d.get("precio", "?"),
            "descuento": d.get("descuento", 0),
            "url": d.get("url", "#"),
            "imagen": d.get("imagen", "/static/placeholder.jpg"),
            "fecha": str(d.get("fecha", ""))
        } for d in datos])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/deportes')
def deportes():
    try:
        datos = list(db["publicados_deports"].find().sort("fecha", -1).limit(6))
        return jsonify([{
            "titulo": d.get("titulo", "Sin título"),
            "precio": d.get("precio", "?"),
            "descuento": d.get("descuento", 0),
            "url": d.get("url", "#"),
            "imagen": d.get("imagen", "/static/placeholder.jpg"),
            "fecha": str(d.get("fecha", ""))
        } for d in datos])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
