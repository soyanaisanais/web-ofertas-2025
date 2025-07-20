from flask import Flask, jsonify, render_template_string
from pymongo import MongoClient
import os

app = Flask(__name__)

# Configuración de MongoDB
MONGO_URI = os.getenv("MONGO_URI") or "mongodb+srv://soyanaisanais:Eduardo1981@cluster0.yaamkjc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "Chollos_2025"
COLLECTION_NAME = "Ultimas_Ofertas"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
coleccion = db[COLLECTION_NAME]

def render_oferta(doc):
    imagen = doc.get('imagen') or doc.get('img') or ''
    titulo = doc.get('titulo', 'Sin título')
    precio = doc.get('precio', 'Sin precio')
    descuento = doc.get('descuento', 0)
    url = doc.get('url', '#')

    return f"""
    <div class='oferta'>
      <img src="{imagen}" alt="Imagen" class="img-oferta"><br>
      <strong>{titulo}</strong><br>
      {precio} <span class='descuento'>(-{descuento}%)</span><br>
      <a href="{url}" target="_blank">Ver oferta</a>
    </div>
    """

def render_categoria(nombre_categoria, filtro):
    docs = list(coleccion.find(filtro).sort("fecha", -1).limit(10))
    if not docs:
        return f"<div id='{nombre_categoria}'>Sin ofertas disponibles</div>"

    primera = render_oferta(docs[0])
    extras = ''.join([render_oferta(d) for d in docs[1:]])

    return f"""
    <div id='{nombre_categoria}'>
      {primera}
      <div class='extra' id='extra-{nombre_categoria}' style='display:none;'>
        {extras}
      </div>
      <span class='ver-mas' onclick="document.getElementById('extra-{nombre_categoria}').style.display = 'block'; this.style.display = 'none';">Ver más</span>
    </div>
    """

@app.route('/')
def home():
    html = f"""
    <html><head>
    <meta charset='UTF-8'>
    <style>
      body {{ background: #111; color: white; font-family: sans-serif; text-align: center; }}
      .oferta {{ border: 1px solid #444; margin: 10px; padding: 10px; border-radius: 10px; background: #222; }}
      .img-oferta {{ max-width: 100%; height: auto; border-radius: 8px; }}
      .ver-mas {{ cursor: pointer; color: #00f; font-weight: bold; display: inline-block; margin-top: 10px; }}
      .descuento {{ color: #0f0; }}
      .contenedor {{ display: flex; justify-content: space-around; flex-wrap: wrap; }}
      .columna {{ width: 30%; min-width: 280px; }}
    </style>
    </head><body>
    <h1>CHOLLOS 2025</h1>
    <div class='contenedor'>
      <div class='columna'>
        <h2>General</h2>
        {render_categoria('general', {})}
      </div>
      <div class='columna'>
        <h2>Electrónica</h2>
        {render_categoria('electronica', {"categoria": "Electronics"})}
      </div>
      <div class='columna'>
        <h2>Deportes</h2>
        {render_categoria('deportes', {"categoria": "Sports"})}
      </div>
    </div>
    </body></html>
    """
    return render_template_string(html)

@app.route('/api/<categoria>')
def api_categoria(categoria):
    if categoria == "general":
        docs = list(coleccion.find({}).sort("fecha", -1).limit(10))
    elif categoria == "electronica":
        docs = list(coleccion.find({"categoria": "Electronics"}).sort("fecha", -1).limit(10))
    elif categoria == "deportes":
        docs = list(coleccion.find({"categoria": "Sports"}).sort("fecha", -1).limit(10))
    else:
        return jsonify({"error": "Categoría no válida"}), 404

    return jsonify([{
        "titulo": d.get("titulo"),
        "precio": d.get("precio"),
        "descuento": d.get("descuento"),
        "url": d.get("url"),
        "imagen": d.get("imagen") or d.get("img")
    } for d in docs])

if __name__ == '__main__':
    app.run(debug=True)
