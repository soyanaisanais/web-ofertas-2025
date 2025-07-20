from flask import Flask, jsonify, render_template, send_from_directory
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')

# Configuración mejorada para MongoDB
MONGO_URI = "mongodb+srv://soyanaisanais:Eduardo1981@cluster0.yaamkjc.mongodb.net/Chollos_2025?retryWrites=true&w=majority&socketTimeoutMS=30000"
client = MongoClient(MONGO_URI)
db = client["Chollos_2025"]

@app.route('/')
def home():
    return render_template('index.html')

# Ruta para archivos estáticos (QR)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

def procesar_ofertas(coleccion):
    try:
        ofertas = list(db[coleccion].find().sort("fecha", -1).limit(6))
        resultado = []
        for oferta in ofertas:
            # Aseguramos que la imagen tenga URL válida
            imagen = oferta.get("imagen", "")
            if not imagen.startswith(('http://', 'https://')):
                imagen = "https://via.placeholder.com/300x200?text=Imagen+no+disponible"
            elif imagen.startswith('http://'):
                imagen = imagen.replace('http://', 'https://')
                
            resultado.append({
                "_id": str(oferta["_id"]),
                "titulo": oferta.get("titulo", "Producto sin título"),
                "precio": oferta.get("precio", "Consultar precio"),
                "descuento": oferta.get("descuento", 0),
                "url": oferta.get("url", "#"),
                "imagen": imagen
            })
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/general')
def general():
    return procesar_ofertas("Ultimas_Ofertas")

@app.route('/api/electronica')
def electronica():
    return procesar_ofertas("publicados_electronica")

@app.route('/api/deportes')
def deportes():
    return procesar_ofertas("publicados_deportes")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
