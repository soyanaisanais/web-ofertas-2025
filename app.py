from flask import Flask, jsonify, render_template, send_from_directory
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# Configuración para archivos estáticos (QR)
app.static_folder = 'static'
app.static_url_path = '/static'

# Conexión a MongoDB (TUS CREDENCIALES ORIGINALES)
MONGO_URI = "mongodb+srv://soyanaisanais:Eduardo1981@cluster0.yaamkjc.mongodb.net/Chollos_2025?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["Chollos_2025"]

# Headers para evitar caché
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/general')
def general():
    try:
        datos = list(db["Ultimas_Ofertas"].find().sort("fecha", -1).limit(6))
        for d in datos:
            d['_id'] = str(d['_id'])
            # Corrige URLs de imágenes rotas
            if 'imagen' not in d or not isinstance(d['imagen'], str) or not d['imagen'].startswith(('http', 'https')):
                d['imagen'] = 'https://via.placeholder.com/300x200?text=Producto+sin+imagen'
            elif 'http://' in d['imagen']:  # Fuerza HTTPS
                d['imagen'] = d['imagen'].replace('http://', 'https://')
        return jsonify(datos)
    except Exception as e:
        return jsonify({"error": f"Error en general: {str(e)}"}), 500

@app.route('/api/electronica')
def electronica():
    try:
        datos = list(db["publicados_electronica"].find().sort("fecha", -1).limit(6))
        for d in datos:
            d['_id'] = str(d['_id'])
            if 'imagen' not in d or not isinstance(d['imagen'], str) or not d['imagen'].startswith(('http', 'https')):
                d['imagen'] = 'https://via.placeholder.com/300x200?text=Electrónica+sin+imagen'
            elif 'http://' in d['imagen']:
                d['imagen'] = d['imagen'].replace('http://', 'https://')
        return jsonify(datos)
    except Exception as e:
        return jsonify({"error": f"Error en electrónica: {str(e)}"}), 500

@app.route('/api/deportes')
def deportes():
    try:
        datos = list(db["publicados_deportes"].find().sort("fecha", -1).limit(6))
        for d in datos:
            d['_id'] = str(d['_id'])
            if 'imagen' not in d or not isinstance(d['imagen'], str) or not d['imagen'].startswith(('http', 'https')):
                d['imagen'] = 'https://via.placeholder.com/300x200?text=Deportes+sin+imagen'
            elif 'http://' in d['imagen']:
                d['imagen'] = d['imagen'].replace('http://', 'https://')
        return jsonify(datos)
    except Exception as e:
        return jsonify({"error": f"Error en deportes: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
