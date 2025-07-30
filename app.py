from flask import Flask, jsonify, render_template, send_from_directory
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

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

def get_ofertas(collection_name, horas=24):
    try:
        # Busca en las últimas X horas (24 por defecto)
        ofertas = list(db[collection_name].find({
            "fecha": {"$gte": datetime.now() - timedelta(hours=horas)}
        }).sort("fecha", -1).limit(10))
        
        resultado = []
        for oferta in ofertas:
            # Compatibilidad con campos de imagen alternativos
            imagen = oferta.get("imagen") or oferta.get("img") or ""
            if not imagen.startswith(('http://', 'https://')):
                imagen = "https://via.placeholder.com/300x200?text=Sin+imagen"
            
            # Asegura formato numérico para precios y descuentos
            precio_num = float(oferta.get("precio_num", oferta.get("precio", 0)))
            descuento = int(oferta.get("descuento", 0))
            
            resultado.append({
                "id": str(oferta.get("_id")),
                "titulo": oferta.get("titulo", "Producto sin título"),
                "precio": precio_num,
                "precio_mostrar": f"{precio_num:.2f} €",
                "descuento": descuento,
                "url": oferta.get("url", "#"),
                "imagen": imagen,
                "fecha": oferta.get("fecha", datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            })
        return resultado
    except Exception as e:
        print(f"Error en {collection_name}: {str(e)}")
        return []

@app.route('/api/general')
def api_general():
    return jsonify(get_ofertas("Ultimas_Ofertas"))

@app.route('/api/electronica')
def api_electronica():
    return jsonify(get_ofertas("publicados_electronica"))

@app.route('/api/deportes')
def api_deportes():
    return jsonify(get_ofertas("publicados_deportes"))

@app.route('/api/moda')
def api_moda():
    return jsonify(get_ofertas("chollos_moda"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
