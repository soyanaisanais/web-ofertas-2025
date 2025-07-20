from flask import Flask, render_template, jsonify
import os
from pymongo import MongoClient

app = Flask(__name__)

# Cargar configuración desde variables de entorno
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DATABASE_NAME", "Chollos_2025")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "Ultimas_Ofertas")

# Conexión a MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Página principal
@app.route('/')
def index():
    return render_template("index.html")

# API para cada categoría
@app.route('/api/<categoria>')
def get_categoria(categoria):
    doc = collection.find_one({"categoria": categoria})
    if doc:
        return jsonify({
            "texto": doc.get("texto", ""),
            "extras": doc.get("extras", [])
        })
    return jsonify({
        "texto": "Sin datos",
        "extras": []
    })

# Iniciar si se ejecuta localmente
if __name__ == '__main__':
    app.run(debug=True)
