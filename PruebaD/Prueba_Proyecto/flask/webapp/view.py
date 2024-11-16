from flask import jsonify, request
from pymongo import MongoClient
from . import app
from datetime import datetime
import os
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import render_template

client = None

#Para trabajar con el contenedor
@app.before_request
def initialize_db():
    global client
    mongo_uri = os.environ.get("MONGO_URI")
    client = MongoClient(mongo_uri)

#_______________________________________________________________________________________________________
@app.route('/')
def home():
    #return jsonify({"message": "Bienvenido al servicio de generacion de citas medicas "}), 200
    return render_template('inicio.html')

#_______________________________________________________________________________________________________
# Ruta para cargar el formulario de inicio de sesión
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('sesion.html')

# Ruta para manejar la autenticación
@app.route('/login', methods=['POST'])
def login():
    db = client["proyecto"]
    usuarios_collection = db["usuarios"]
    data = request.json
    
    # Validación de entrada
    username = data.get("usuario")
    password = data.get("password")
    if not username or not password:
        return jsonify({"message": "Usuario y contraseña son requeridos"}), 400

    # Buscar usuario en la colección
    usuario = usuarios_collection.find_one({"usuario": username})
    if usuario and check_password_hash(usuario["password"], password):
        return jsonify({"message": "Login exitoso"}), 200
    
    return jsonify({"message": "Usuario o contraseña incorrectos"}), 401
#_________________________________________________________________________________________________________
@app.route('/registro', methods=['GET'])
def crear_usuario_page():
    return render_template('registro.html')

@app.route('/registro', methods=['POST'])
def crear_usuario():
    db = client["proyecto"]
    usuarios_collection = db["usuarios"]
    data = request.json
    
    # Validación de entrada
    username = data.get("usuario")
    password = data.get("password")
    if not username or not password:
        return jsonify({"message": "Usuario y contraseña son requeridos"}), 400

    # Verificar si el usuario ya existe
    if usuarios_collection.find_one({"usuario": username}):
        return jsonify({"message": "El usuario ya existe"}), 409
    
    # Crear el nuevo usuario con contraseña cifrada
    nuevo_usuario = {
        "usuario": username,
        "password": generate_password_hash(password)
    }
    usuarios_collection.insert_one(nuevo_usuario)
    return jsonify({"message": "Usuario creado exitosamente"}), 201

#_________________________________________________________________________________________________________

@app.route('/menu_cita')
def menu_cita():
    return render_template('menu_cita.html')

#_______________________________________________________________________________________________________

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
    return jsonify({"message": "Cita creada", "numeroDeCita": numero_de_cita}), 201

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
            "nombre": cita.get("nombre", ""),
            "fechaCita": cita.get("fechaCita", ""),
            "hora": cita.get("hora", ""),
            "descripcion": cita.get("descripcion", ""),
            "numeroDeCita": cita.get("numeroDeCita", ""),
            "fechaActualizacionCita": cita.get("fechaActualizacion","")
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


#____________________________________________________________________________________________________
# Eliminar una cita
@app.route('/borrar_cita', methods=['GET'])
def borrar_cita_page():
    return render_template('borrar_cita.html')

@app.route('/borrar_cita', methods=['DELETE'])
def eliminar_cita():
    # Extraer los datos del cuerpo de la solicitud
    data = request.get_json()
    numeroDeCita = data.get("numeroDeCita")

    # Verificar que el número de cita exista
    if not numeroDeCita:
        return jsonify({"message": "Número de cita no proporcionado"}), 400

    # Conectar a la base de datos y eliminar
    db = client["proyecto"]
    citas_collection = db["citas"]
    delete_result = citas_collection.delete_one({"numeroDeCita": numeroDeCita})
    
    if delete_result.deleted_count == 1:
        return jsonify({"message": "Cita eliminada"}), 200
    return jsonify({"message": "Cita no encontrada. Reintente"}), 404

#___________________________________________________________________________________________________

if __name__== '_main_':
    app.run(debug=True)

