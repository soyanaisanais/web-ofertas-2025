from flask import Flask, render_template, jsonify
import os
from pymongo import MongoClient

app = Flask(__name__)

# Configuración de MongoDB
MONGO_URI = os.getenv("MONGO_URI") or "mongodb+srv://soyanaisanais:Eduardo1981@cluster0.yaamkjc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "Chollos_2025"
COLLECTION_NAME = "Ultimas_Ofertas"

# Conexión a MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/general')
def get_general():
    docs = list(collection.find().sort("fecha", -1))
    if not docs:
        return jsonify({"texto": "Sin datos disponibles", "extras": []})
    primero = docs[0]
    extras = docs[1:10]
    return jsonify({
        "texto": render_oferta(primero),
        "extras": [render_oferta(e) for e in extras]
    })

@app.route('/api/electronica')
def get_electronica():
    docs = list(collection.find({"categoria": {"$regex": "electro", "$options": "i"}}).sort("fecha", -1))
    if not docs:
        return jsonify({"texto": "Próximamente…", "extras": []})
    primero = docs[0]
    extras = docs[1:10]
    return jsonify({
        "texto": render_oferta(primero),
        "extras": [render_oferta(e) for e in extras]
    })

@app.route('/api/deportes')
def get_deportes():
    docs = list(collection.find({"categoria": {"$regex": "deporte", "$options": "i"}}).sort("fecha", -1))
    if not docs:
        return jsonify({"texto": "Próximamente…", "extras": []})
    primero = docs[0]
    extras = docs[1:10]
    return jsonify({
        "texto": render_oferta(primero),
        "extras": [render_oferta(e) for e in extras]
    })

def render_oferta(doc):
    return f"""
    <div style='text-align:center'>
      <img src="{doc.get('img', '')}" alt="Imagen" style="width:100px"><br>
      <strong>{doc.get('titulo', '')}</strong><br>
      {doc.get('precio', '')} <span style='color:green'>(-{doc.get('descuento', 0)}%)</span><br>
      <a href="{doc.get('url', '#')}" target="_blank">Ver oferta</a>
    </div>
    <hr>
    """

if __name__ == '__main__':
    app.run(debug=True)
