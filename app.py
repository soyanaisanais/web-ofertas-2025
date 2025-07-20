from flask import Flask, jsonify, render_template, send_from_directory
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')

# Conexión a MongoDB (usa tus credenciales)
MONGO_URI = "mongodb+srv://soyanaisanais:Eduardo1981@cluster0.yaamkjc.mongodb.net/Chollos_2025?retryWrites=true&w=majority&socketTimeoutMS=30000"
client = MongoClient(MONGO_URI)
db = client["Chollos_2025"]

# Configuración importante para evitar errores
@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self' https: data:"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

def obtener_ofertas(nombre_coleccion):
    try:
        # Busca en ambas colecciones por si hay diferencias
        coleccion = db[nombre_coleccion]
        ofertas = list(coleccion.find().sort("fecha", -1).limit(6))
        
        resultado = []
        for oferta in ofertas:
            # Compatibilidad con 'imagen' o 'img'
            imagen_url = oferta.get('imagen') or oferta.get('img', '')
            
            # Fuerza HTTPS si es HTTP
            if imagen_url.startswith('http://'):
                imagen_url = imagen_url.replace('http://', 'https://')
            
            # Si no hay imagen válida, usa un placeholder
            if not imagen_url.startswith('https://'):
                imagen_url = 'https://via.placeholder.com/300x200?text=Imagen+no+disponible'
            
            resultado.append({
                "id": str(oferta.get("_id")),
                "titulo": oferta.get("titulo", "Producto sin título"),
                "precio": oferta.get("precio", "Consultar precio"),
                "descuento": oferta.get("descuento", 0),
                "url": oferta.get("url", "#"),
                "imagen": imagen_url,
                "fecha": oferta.get("fecha", datetime.utcnow()).strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return jsonify(resultado)
    
    except Exception as e:
        print(f"⚠️ Error en {nombre_coleccion}: {str(e)}")
        return jsonify({"error": f"Error al cargar {nombre_coleccion}"}), 500

@app.route('/api/general')
def general():
    return obtener_ofertas("Ultimas_Ofertas")

@app.route('/api/electronica')
def electronica():
    return obtener_ofertas("publicados_electronica")

@app.route('/api/deportes')
def deportes():
    return obtener_ofertas("publicados_deportes")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
