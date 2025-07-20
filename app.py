from flask import Flask, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# Conexión a MongoDB (TUS CREDENCIALES ORIGINALES)
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
        for d in datos:
            d['_id'] = str(d['_id'])
            # Asegurar que la imagen tenga URL válida
            if 'imagen' not in d or not d['imagen'].startswith(('http', 'https')):
                d['imagen'] = 'https://via.placeholder.com/300?text=Imagen+no+disponible'
        return jsonify(datos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/electronica')
def electronica():
    try:
        datos = list(db["publicados_electronica"].find().sort("fecha", -1).limit(6))
        for d in datos:
            d['_id'] = str(d['_id'])
            if 'imagen' not in d or not d['imagen'].startswith(('http', 'https')):
                d['imagen'] = 'https://via.placeholder.com/300?text=Imagen+no+disponible'
        return jsonify(datos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/deportes')
def deportes():
    try:
        datos = list(db["publicados_deportes"].find().sort("fecha", -1).limit(6))
        for d in datos:
            d['_id'] = str(d['_id'])
            if 'imagen' not in d or not d['imagen'].startswith(('http', 'https')):
                d['imagen'] = 'https://via.placeholder.com/300?text=Imagen+no+disponible'
        return jsonify(datos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
