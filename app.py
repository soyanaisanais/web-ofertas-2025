from flask import Flask, jsonify, render_template, send_from_directory
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')

# Conexión a MongoDB (usa tus credenciales)
MONGO_URI = "mongodb+srv://soyanaisanais:Eduardo1981@cluster0.yaamkjc.mongodb.net/Chollos_2025?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["Chollos_2025"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

def get_ofertas(collection_name):
    try:
        # Busca tanto 'imagen' como 'img' en la base de datos
        ofertas = list(db[collection_name].find().sort("fecha", -1).limit(6))
        resultado = []
        for oferta in ofertas:
            imagen = oferta.get("imagen") or oferta.get("img") or ""
            if not imagen.startswith(('http://', 'https://')):
                imagen = "https://via.placeholder.com/300x200?text=Imagen+no+disponible"

            resultado.append({
                "id": str(oferta.get("_id")),
                "titulo": oferta.get("titulo", "Producto sin título"),
                "precio": oferta.get("precio", "Consultar"),
                "descuento": oferta.get("descuento", 0),
                "url": oferta.get("url", "#"),
                "imagen": imagen
            })
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/general')
def general():
    return get_ofertas("Ultimas_Ofertas")

@app.route('/api/electronica')
def electronica():
    return get_ofertas("publicados_electronica")

@app.route('/api/deportes')
def deportes():
    return get_ofertas("publicados_deportes")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
