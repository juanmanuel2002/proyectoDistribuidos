from flask import jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from . import app
import os

client = None

@app.before_request
def initialize_db():
    global client
    mongo_uri = os.environ.get("MONGO_URI")
    client = MongoClient(mongo_uri)


@app.route('/')
def home():
    return jsonify({"message": "Esto demuestra que si encuentra la instancia"}), 200

# Crear una nueva cita
@app.route('/crear/cita', methods=['POST'])
def crear_cita():
    db = client["proyecto"]
    citas_collection = db["citas"]
    data = request.json
    cita = {
        "nombre": data.get("nombre"),
        "fecha": data.get("fecha"),
        "hora": data.get("hora"),
        "descripcion": data.get("descripcion")
    }
    result = citas_collection.insert_one(cita)
    return jsonify({"message": "Cita creada", "id": str(result.inserted_id)}), 201

# Consultar todas las citas
@app.route('/ver/citas', methods=['GET'])
def obtener_citas():
    db = client["proyecto"]
    citas_collection = db["citas"]
    citas = []
    for cita in citas_collection.find():
        citas.append({
            "id": str(cita["_id"]),
            "nombre": cita["nombre"],
            "fecha": cita["fecha"],
            "hora": cita["hora"],
            "descripcion": cita["descripcion"]
        })
    return jsonify(citas), 200

# Consultar una cita por ID
@app.route('/consultar/cita/<id>', methods=['GET'])
def obtener_cita(id):
    db = client["proyecto"]
    citas_collection = db["citas"]
    cita = citas_collection.find_one({"_id": ObjectId(id)})
    if cita:
        return jsonify({
            "id": str(cita["_id"]),
            "nombre": cita["nombre"],
            "fecha": cita["fecha"],
            "hora": cita["hora"],
            "descripcion": cita["descripcion"]
        }), 200
    return jsonify({"message": "Cita no encontrada"}), 404

# Actualizar una cita
@app.route('/modificar/cita/<id>', methods=['PUT'])
def actualizar_cita(id):
    db = client["proyecto"]
    citas_collection = db["citas"]
    data = request.json
    update_result = citas_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "nombre": data.get("nombre"),
            "fecha": data.get("fecha"),
            "hora": data.get("hora"),
            "descripcion": data.get("descripcion")
        }}
    )
    if update_result.matched_count == 1:
        return jsonify({"message": "Cita actualizada"}), 200
    return jsonify({"message": "Cita no encontrada"}), 404

# Eliminar una cita
@app.route('/borrar/cita/<id>', methods=['DELETE'])
def eliminar_cita(id):
    db = client["proyecto"]
    citas_collection = db["citas"]
    delete_result = citas_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return jsonify({"message": "Cita eliminada"}), 200
    return jsonify({"message": "Cita no encontrada"}), 404

if __name__== '_main_':
    app.run(debug=True)
