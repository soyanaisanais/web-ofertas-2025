from flask import Flask, render_template, jsonify, send_from_directory
from pymongo import MongoClient
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Conexión MongoDB (tus credenciales)
MONGO_URI = "mongodb+srv://soyanaisanais:Eduardo1981@cluster0.yaamkjc.mongodb.net/Chollos_2025?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["Chollos_2025"]

# Ruta para archivos estáticos (CSS/JS/imágenes)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# Rutas API
@app.route('/api/general')
def api_general():
    return obtener_ofertas("Ultimas_Ofertas")

@app.route('/api/electronica')
def api_electronica():
    return obtener_ofertas("publicados_electronica")

@app.route('/api/deportes')
def api_deportes():
    return obtener_ofertas("publicados_deports")

def obtener_ofertas(coleccion):
    try:
        datos = list(db[coleccion].find().limit(6))
        return jsonify([{
            "titulo": d.get("titulo", ""),
            "precio": d.get("precio", ""),
            "descuento": d.get("descuento", 0),
            "url": d.get("url", "#"),
            "imagen": d.get("imagen", "")
        } for d in datos])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta principal
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
