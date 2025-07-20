from flask import Flask, jsonify, render_template_string
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# Configuración de MongoDB (usa tus credenciales existentes)
MONGO_URI = "mongodb+srv://soyanaisanais:Eduardo1981@cluster0.yaamkjc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "Chollos_2025"
COLLECTION_NAME = "Ultimas_Ofertas"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
coleccion = db[COLLECTION_NAME]

# Plantilla HTML base con todos los estilos
HTML_BASE = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chollos 2025</title>
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Poppins:wght@400;700&display=swap" rel="stylesheet">
  <style>
    body {
      margin: 0;
      font-family: 'Poppins', sans-serif;
      background: #1a1a1a;
      color: #f1f1f1;
    }
    header {
      background-color: #000;
      padding: 50px 20px 30px;
      text-align: center;
    }
    .title-3d {
      font-family: 'Orbitron', sans-serif;
      font-size: 3.5em;
      color: #ffd700;
      text-shadow: 2px 2px 0 #000, 4px 4px 5px #333;
      display: inline-block;
      border: 3px solid #000;
      padding: 20px 40px;
      border-radius: 20px;
      background: linear-gradient(145deg, #fff6b0, #ffd700);
    }
    .sections {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 25px;
      padding: 40px 20px;
      background-color: #eee;
    }
    .card {
      background: #f9f9f9;
      border-radius: 12px;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
      width: 320px;
      padding: 25px;
      border: 1px solid #ccc;
      color: #111;
    }
    .card h2 {
      font-size: 1.4em;
      color: #000;
      background: #ffd700;
      padding: 10px;
      border-radius: 8px;
      text-align: center;
      border: 2px solid #000;
      text-shadow: 1px 1px 2px #000;
    }
    .oferta {
      text-align: center;
      margin-top: 15px;
    }
    .oferta img {
      max-width: 100%;
      height: auto;
      border-radius: 10px;
    }
    .oferta h3 {
      font-size: 1em;
      margin: 10px 0;
    }
    .oferta p {
      margin: 5px 0;
    }
    .ver-mas, .ver-menos {
      display: block;
      text-align: center;
      margin-top: 15px;
      color: #1e90ff;
      font-weight: bold;
      cursor: pointer;
    }
    .extra {
      display: none;
    }
    .qr {
      text-align: center;
      margin: 40px auto;
    }
    .qr img {
      width: 170px;
      border-radius: 12px;
      background: #fff;
      padding: 8px;
      box-shadow: 0 4px 15px rgba(255, 255, 255, 0.1);
    }
    footer {
      background: #ccc;
      text-align: center;
      font-size: 0.8em;
      color: #222;
      padding: 20px;
      margin-top: 60px;
    }
    .error {
      color: red;
      padding: 10px;
    }
  </style>
</head>
<body>
  <header>
    <h1 class="title-3d">Chollos 2025</h1>
  </header>
  {contenido}
  <div class="qr">
    <img src="/static/canal_qr.png" alt="QR del canal de Telegram">
  </div>
  <footer>
    Esta es una página de afiliados. No vendemos productos directamente. Las ofertas y ventas pertenecen a terceros.
  </footer>
  <script>
    function verMas(cat) {
      document.getElementById(`extra-${cat}`).style.display = 'block';
      document.querySelector(`#${cat} .ver-mas`).style.display = 'none';
      document.querySelector(`#${cat} .ver-menos`).style.display = 'block';
    }
    function verMenos(cat) {
      document.getElementById(`extra-${cat}`).style.display = 'none';
      document.querySelector(`#${cat} .ver-mas`).style.display = 'block';
      document.querySelector(`#${cat} .ver-menos`).style.display = 'none';
    }
  </script>
</body>
</html>
"""

def generar_oferta_html(oferta):
    return f"""
    <div class="oferta">
      <img src="{oferta.get('imagen', oferta.get('img', ''))}" alt="Imagen">
      <h3>{oferta.get('titulo', 'Sin título')}</h3>
      <p>{oferta.get('precio', '?')} <span style="color:green">(-{oferta.get('descuento', 0)}%)</span></p>
      <a href="{oferta.get('url', '#')}" target="_blank">Ver oferta</a>
    </div>
    """

@app.route('/')
def home():
    try:
        # Obtener ofertas para cada categoría
        general = list(coleccion.find({}).sort("fecha", -1).limit(5))
        electronica = list(coleccion.find({"categoria": "Electronics"}).sort("fecha", -1).limit(5))
        deportes = list(coleccion.find({"categoria": "Sports"}).sort("fecha", -1).limit(5))

        # Generar HTML para cada categoría
        def generar_seccion(cat, datos):
            if not datos:
                return f'<div id="{cat}"><p class="error">No hay ofertas</p></div>'
            
            principal = generar_oferta_html(datos[0])
            extras = ''.join([generar_oferta_html(d) for d in datos[1:]])
            
            return f"""
            <div id="{cat}">
              {principal}
              <div class="extra" id="extra-{cat}">
                {extras}
              </div>
              <span class="ver-mas" onclick="verMas('{cat}')">Ver más</span>
              <span class="ver-menos" onclick="verMenos('{cat}')" style="display:none;">Ver menos</span>
            </div>
            """

        contenido = f"""
        <div class="sections">
          <div class="card">
            <h2>Chollos 2025</h2>
            {generar_seccion('general', general)}
          </div>
          <div class="card">
            <h2>Chollos Electrónica</h2>
            {generar_seccion('electronica', electronica)}
          </div>
          <div class="card">
            <h2>Chollos Deportes</h2>
            {generar_seccion('deportes', deportes)}
          </div>
        </div>
        """

        return render_template_string(HTML_BASE.replace("{contenido}", contenido))
    
    except Exception as e:
        error_html = f'<div class="error">Error al cargar ofertas: {str(e)}</div>'
        return render_template_string(HTML_BASE.replace("{contenido}", error_html))

@app.route('/api/<categoria>')
def api_ofertas(categoria):
    try:
        if categoria == "general":
            datos = list(coleccion.find({}).sort("fecha", -1).limit(10))
        elif categoria == "electronica":
            datos = list(coleccion.find({"categoria": "Electronics"}).sort("fecha", -1).limit(10))
        elif categoria == "deportes":
            datos = list(coleccion.find({"categoria": "Sports"}).sort("fecha", -1).limit(10))
        else:
            return jsonify({"error": "Categoría no válida"}), 404

        return jsonify([{
            "imagen": d.get("imagen", d.get("img", "")),
            "titulo": d.get("titulo", "Sin título"),
            "precio": d.get("precio", "?"),
            "descuento": d.get("descuento", 0),
            "url": d.get("url", "#")
        } for d in datos])
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
