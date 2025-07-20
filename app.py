from flask import Flask, jsonify, render_template, send_from_directory
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')

# Conexión MongoDB con seguridad reforzada
MONGO_URI = "mongodb+srv://soyanaisanais:Eduardo1981@cluster0.yaamkjc.mongodb.net/Chollos_2025?retryWrites=true&w=majority&socketTimeoutMS=30000&connectTimeoutMS=30000"
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client.get_database("Chollos_2025")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

def get_products(collection_name):
    try:
        products = list(db[collection_name].find().sort("fecha", -1).limit(6))
        
        # Debug: Ver datos crudos
        print(f"\n🔥 Datos CRUDOS de {collection_name}:")
        for p in products[:1]:  # Solo muestra el primero para no saturar
            print(p)
        
        # Procesamiento a prueba de errores
        result = []
        for p in products:
            # Compatibilidad con 'imagen'/'img' y múltiples formatos
            img_url = str(p.get('imagen') or p.get('img') or '')
            if not img_url.startswith(('http://', 'https://')):
                img_url = f"https://via.placeholder.com/300x200?text={collection_name[:4]}"
            elif img_url.startswith('http://'):
                img_url = img_url.replace('http://', 'https://')
            
            result.append({
                'id': str(p.get('_id')),
                'titulo': str(p.get('titulo', 'Oferta Especial')).strip(),
                'precio': str(p.get('precio', 'Consultar')).strip(),
                'descuento': int(p.get('descuento', 0)),
                'url': str(p.get('url', '#')).strip(),
                'imagen': img_url,
                'fecha': p.get('fecha', datetime.utcnow()).strftime("%d/%m %H:%M")
            })
        
        return jsonify(result)
    
    except Exception as e:
        print(f"⛔ ERROR en {collection_name}: {str(e)}")
        return jsonify({'error': 'Sistema en mantenimiento'}), 500

@app.route('/api/general')
def general():
    return get_products("Ultimas_Ofertas")

@app.route('/api/electronica')
def electronica():
    return get_products("publicados_electronica")

@app.route('/api/deportes')
def deportes():
    return get_products("publicados_deportes")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
