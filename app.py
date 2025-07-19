from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

# Inicializar Flask
app = Flask(__name__)
CORS(app)

# Leer las variables de entorno
mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DATABASE_NAME")
collection_name = os.environ.get("COLLECTION_NAME")

# Conexión a MongoDB
cliente = MongoClient(mongo_uri)
db = cliente[db_name]
coleccion = db[collection_name]

# Ruta principal
@app.route('/')
def inicio():
    return "🚀 Web de ofertas activa y funcionando correctamente."

# Ruta para obtener las ofertas
@app.route('/ofertas')
def obtener_ofertas():
    datos = list(coleccion.find({}, {"_id": 0}))  # Excluye el _id
    return jsonify(datos)

# Iniciar servidor (solo en local)
if __name__ == '__main__':
    app.run(debug=True)
