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

def obtener_ofertas(coleccion):
    try:
        # Obtener 6 productos más recientes
        productos = list(db[coleccion].find().sort("fecha", -1).limit(6))
        
        resultado = []
        for p in productos:
            # Compatibilidad con 'imagen' o 'img'
            imagen = p.get('imagen') or p.get('img', '')
            if not imagen.startswith('http'):
                imagen = f'https://via.placeholder.com/300x200?text={coleccion[:4]}'
            
            # Limpiar precio
            precio = str(p.get('precio', 'Consultar')).replace('\xa0', ' ').strip()
            
            resultado.append({
                'id': str(p['_id']),
                'titulo': p.get('titulo', 'Producto sin título'),
                'precio': precio,
                'descuento': int(p.get('descuento', 0)),
                'url': p.get('url', '#'),
                'imagen': imagen,
                'fecha': p.get('fecha', datetime.utcnow()).strftime("%d/%m %H:%M")
            })
        
        return jsonify(resultado)
    
    except Exception as e:
        print(f"Error en {coleccion}: {str(e)}")
        return jsonify({'error': 'Datos no disponibles'}), 500

@app.route('/api/Chollos_2025')  # ← Ruta modificada
def chollos_2025():
    return obtener_ofertas("Ultimas_Ofertas")  # Nombre real en MongoDB

@app.route('/api/electronica')
def electronica():
    return obtener_ofertas("publicados_electronica")

@app.route('/api/deportes')
def deportes():
    return obtener_ofertas("publicados_deportes")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
