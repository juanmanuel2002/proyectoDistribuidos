from flask import jsonify, request
from pymongo import MongoClient
from . import app
from datetime import datetime
import os

client = None

#Para trabajar con el contenedor
@app.before_request
def initialize_db():
    global client
    mongo_uri = os.environ.get("MONGO_URI")
    client = MongoClient(mongo_uri)


@app.route('/')
def home():
    return jsonify({"message": "Bienvenido al servicio de generacion de citas medicas "}), 200

# Crear una nueva cita
@app.route('/crear/cita', methods=['POST'])
def crear_cita():
    db = client["proyecto"]
    citas_collection = db["citas"]
    data = request.json
     # Lista de propiedades permitidas
    propiedades_permitidas = {"nombre", "fecha", "hora", "descripcion"}
    
    # Validación: Verifica que no haya propiedades adicionales
    if not propiedades_permitidas.issuperset(data.keys()):
        return jsonify({"error": "Propiedades no permitidas en el cuerpo de la solicitud"}), 400

     # Agregar fecha de creación
    fecha_creacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

     # Generar el prefijo de numeroDeCita
    fecha_actual = datetime.now().strftime("%y%m%d")
    citas_hoy = citas_collection.count_documents({"numeroDeCita": {"$regex": f"^C{fecha_actual}"}}) + 1
    numero_de_cita = f"C{fecha_actual}{citas_hoy:03}"

    cita = {
        "nombre": data.get("nombre"),
        "fechaCita": data.get("fecha"),
        "hora": data.get("hora"),
        "descripcion": data.get("descripcion"),
        "fechaDeCreacion": fecha_creacion,
        "numeroDeCita": numero_de_cita
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
            "nombre": cita.get("nombre", ""),
            "fechaCita": cita.get("fechaCita", ""),
            "hora": cita.get("hora", ""),
            "descripcion": cita.get("descripcion", ""),
            "numeroDeCita": cita.get("numeroDeCita", ""),
            "fechaActualizacionCita": cita.get("fechaActualizacion","")
        })
    return jsonify(citas), 200

# Consultar una cita por ID
@app.route('/consultar/cita/<numeroDeCita>', methods=['GET'])
def obtener_cita(numeroDeCita):
    db = client["proyecto"]
    citas_collection = db["citas"]
    cita = citas_collection.find_one({"numeroDeCita": numeroDeCita})
    if cita:
        return jsonify({
            "id": str(cita["_id"]),
            "nombre": cita["nombre"],
            "fechaCita": cita["fechaCita"],
            "hora": cita["hora"],
            "descripcion": cita["descripcion"]
        }), 200
    return jsonify({"message": "Cita no encontrada"}), 404

# Actualizar una cita
@app.route('/modificar/cita/<numeroDeCita>', methods=['PUT'])
def actualizar_cita(numeroDeCita):
    db = client["proyecto"]
    citas_collection = db["citas"]
    data = request.json
    # Lista de propiedades permitidas
    propiedades_permitidas = {"nombre", "fecha", "hora", "descripcion"}
    
    # Validación: Verifica que no haya propiedades adicionales
    if not propiedades_permitidas.issuperset(data.keys()):
        return jsonify({"error": "Propiedades no permitidas en el cuerpo de la solicitud"}), 400

     # Agregar fecha de creación
    fecha_actualizacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    update_result = citas_collection.update_one(
        {"numeroDeCita": numeroDeCita},
        {"$set": {
            "nombre": data.get("nombre"),
            "fechaCita": data.get("fecha"),
            "hora": data.get("hora"),
            "descripcion": data.get("descripcion"),
            "fechaActualizacion":fecha_actualizacion
        }}
    )
    if update_result.matched_count == 1:
        return jsonify({"message": "Cita actualizada"}), 200
    return jsonify({"message": "Cita no encontrada"}), 404

# Eliminar una cita
@app.route('/borrar/cita/<numeroDeCita>', methods=['DELETE'])
def eliminar_cita(numeroDeCita):
    db = client["proyecto"]
    citas_collection = db["citas"]
    delete_result = citas_collection.delete_one({"numeroDeCita": numeroDeCita})
    if delete_result.deleted_count == 1:
        return jsonify({"message": "Cita eliminada"}), 200
    return jsonify({"message": "Cita no encontrada"}), 404

if __name__== '_main_':
    app.run(debug=True)

