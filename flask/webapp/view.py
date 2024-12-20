from flask import jsonify, request
from pymongo import MongoClient
from . import app
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template
from flask import redirect, url_for

client = None

# Para trabajar con el contenedor
@app.before_request
def initialize_db():
    global client
    mongo_uri = os.environ.get("MONGO_URI")
    client = MongoClient(mongo_uri)

# Ruta de inicio
@app.route('/')
def home():
    return render_template('inicio.html')

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

# Ruta para la página de registro de usuario
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

# Ruta para el menú de citas
@app.route('/menu_cita', methods=['GET'])
def menu_cita():
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
            "fechaActualizacionCita": cita.get("fechaActualizacion", "")
        })
    return render_template('menu_cita.html', citas=citas)



# Ruta para crear una nueva cita

@app.route('/crear/cita', methods=['GET', 'POST'])
def crear_cita():
    if request.method == 'GET':
        return render_template('crear_cita.html')  # Página para crear la cita

    if request.method == 'POST':
        data = request.form  # Obtener datos del formulario

        # Aquí validas los datos recibidos, por ejemplo, nombre, fecha, hora y descripción
        nombre = data.get('nombre')
        fecha_cita = data.get('fechaCita')
        hora = data.get('hora')
        descripcion = data.get('descripcion')

        if not nombre or not fecha_cita or not hora or not descripcion:
            return "Todos los campos son obligatorios", 400
        

        # Guardar la nueva cita en la base de datos
        db = client["proyecto"]
        citas_collection = db["citas"]
        
        # Generar el prefijo de numeroDeCita
        fecha_actual = datetime.now().strftime("%y%m%d")

        # Buscar el mayor numeroDeCita para la fecha actual
        ultima_cita = citas_collection.find_one(
            {"numeroDeCita": {"$regex": f"^C{fecha_actual}"}},
            sort=[("numeroDeCita", -1)]
        )
        if ultima_cita and "numeroDeCita" in ultima_cita:
            ultimo_numero = int(ultima_cita["numeroDeCita"][-3:])  # Extraer los últimos 3 dígitos
        else:
            ultimo_numero = 0
        # Incrementar el número de cita
        siguiente_numero = ultimo_numero + 1
        numero_de_cita = f"C{fecha_actual}{siguiente_numero:03}"

        # Convertir al formato dd/mm/yyyy
        fecha_cita_formateada = datetime.strptime(fecha_cita, "%Y-%m-%d").strftime("%d/%m/%Y")

        # Inserción en la base de datos
        cita = {
            "numeroDeCita": numero_de_cita,
            "nombre": nombre,
            "fechaCita": fecha_cita_formateada,
            "hora": hora,
            "descripcion": descripcion,
            "fechaActualizacion": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }

        citas_collection.insert_one(cita)

        # Redirigir al menú de citas después de crear la cita
        return redirect(url_for('menu_cita'))

# Ruta para consultar todas las citas
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

#obtener cita
@app.route('/consultar/cita/<numeroDeCita>', methods=['GET'])
def consultar_cita(numeroDeCita):
    db = client["proyecto"]
    citas_collection = db["citas"]
    cita = citas_collection.find_one({"numeroDeCita": numeroDeCita})
    if cita:
        return render_template('consultar_cita.html', cita=cita)
    return jsonify({"message": "Cita no encontrada"}), 404



# Ruta para consultar una cita por ID
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

#Modificar cita

@app.route('/modificar/cita/<numeroDeCita>', methods=['GET', 'POST'])
def modificar_cita(numeroDeCita):
    db = client["proyecto"]
    citas_collection = db["citas"]

    if request.method == 'GET':
        # Obtener los detalles de la cita
        cita = citas_collection.find_one({"numeroDeCita": numeroDeCita})
        if cita:
            return render_template("modificar_cita.html", cita=cita)
        return jsonify({"error": "Cita no encontrada"}), 404

    if request.method == 'POST':  # Cambié PUT por POST
        try:
            # Obtener los datos del formulario
            nombre = request.form['nombre']
            fechaCita = request.form['fechaCita']
            hora = request.form['hora']
            descripcion = request.form['comentarios']

            print(f"Datos recibidos: {nombre}, {fechaCita}, {hora}, {descripcion}")  # Agregar para depuración

            # Fecha de actualización - obtenemos la fecha y hora actual del servidor
            fecha_actualizacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            # Convertir al formato dd/mm/yyyy
            fecha_cita_formateada = datetime.strptime(fechaCita, "%Y-%m-%d").strftime("%d/%m/%Y")

            # Actualizar la cita en la base de datos
            update_result = citas_collection.update_one(
                {"numeroDeCita": numeroDeCita},
                {"$set": {
                    "nombre": nombre,
                    "fechaCita": fecha_cita_formateada,
                    "hora": hora,
                    "descripcion": descripcion,
                    "fechaActualizacion": fecha_actualizacion  # Usamos la fecha y hora actuales
                }}
            )

            print(f"Resultado de actualización: {update_result.modified_count}")  # Verificar la cantidad de documentos modificados

            if update_result.matched_count == 1:
                # Redirigir al menú de citas después de la actualización
                return redirect(url_for('menu_cita'))  # 'menu_cita' es el nombre de la ruta que muestra el menú de citas
            return jsonify({"error": "Cita no encontrada"}), 404
        except Exception as e:
            print(f"Error al procesar la solicitud: {str(e)}")  # Mostrar el error en la consola
            return jsonify({"error": "Error en el servidor"}), 500






# Ruta para eliminar una cita
@app.route('/borrar_cita/<numeroDeCita>', methods=['DELETE'])
def eliminar_cita(numeroDeCita):
    db = client["proyecto"]
    citas_collection = db["citas"]
    delete_result = citas_collection.delete_one({"numeroDeCita": numeroDeCita})
    if delete_result.deleted_count == 1:
        return jsonify({"message": "Cita eliminada"}), 200
    return jsonify({"message": "Cita no encontrada"}), 404

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=8003)