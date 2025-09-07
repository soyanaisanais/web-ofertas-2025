from flask import Flask, jsonify, render_template, send_from_directory
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

# Conexión a MongoDB con tus credenciales reales
MONGO_URI = "mongodb+srv://soyanaisanais:Eduardo1981@cluster0.yaamkjc.mongodb.net/Chollos_2025?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["Chollos_2025"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

def get_ofertas(collection_name, horas=24000):
    """
    Obtiene ofertas de la colección indicada.
    Usamos 24000 horas (≈1000 días) para que salgan resultados aunque no sean recientes.
    """
    try:
        desde = datetime.now() - timedelta(hours=horas)
        ofertas_cursor = db[collection_name].find({
            "fecha": {"$gte": desde}
        }).sort("fecha", -1).limit(10)

        ofertas = list(ofertas_cursor)
        resultado = []
        for oferta in ofertas:
            # Imagen: admite 'imagen' o 'img'
            imagen = oferta.get("imagen") or oferta.get("img") or ""
            if not isinstance(imagen, str) or not imagen.startswith(('http://', 'https://')):
                imagen = "https://via.placeholder.com/300x200?text=Sin+imagen"

            # Precio: intenta 'precio_num' o 'precio'
            try:
                precio_num = float(oferta.get("precio_num", oferta.get("precio", 0)) or 0)
            except Exception:
                precio_num = 0.0

            # Descuento: asegura entero
            try:
                descuento = int(oferta.get("descuento", 0) or 0)
            except Exception:
                descuento = 0

            # URL: admite 'URL' (mayúsculas) o 'url' (minúsculas)
            url = oferta.get("URL", oferta.get("url", "#")) or "#"

            # Fecha: formatea si es datetime
            fecha_val = oferta.get("fecha", datetime.now())
            if isinstance(fecha_val, datetime):
                fecha_str = fecha_val.strftime("%Y-%m-%d %H:%M:%S")
            else:
                fecha_str = str(fecha_val)

            resultado.append({
                "id": str(oferta.get("_id")),
                "titulo": oferta.get("titulo", "Producto sin título"),
                "precio": precio_num,
                "precio_mostrar": f"{precio_num:.2f} €",
                "descuento": descuento,
                "url": url,
                "imagen": imagen,
                "fecha": fecha_str
            })
        return resultado
    except Exception as e:
        print(f"Error en {collection_name}: {str(e)}")
        return []

# Rutas de la API
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
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
