from flask import Flask, render_template, request, jsonify
from flask import Flask, request, redirect, url_for, render_template, flash

import requests
import json
import os
import pymysql
import base64
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os



# Configuración para la carpeta de subida
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}



# Conectar a la base de datos
def connect():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='rutags',
        cursorclass=pymysql.cursors.DictCursor
    )

# Función para guardar el reporte
def save_report(bus_id, description, category, image_path=None):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            
            # Convertir imagen a base64
            image_base64 = None
            if image_path:
                with open(image_path, "rb") as img_file:
                    image_base64 = base64.b64encode(img_file.read()).decode('utf-8')

            # Insertar el reporte
            sql = """
            INSERT INTO reportes (bus_id, description, category, image_base64)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (bus_id, description, category, image_base64))
            connection.commit()
            print("✅ Reporte guardado exitosamente.")
    except Exception as e:
        print(f"❌ Error al guardar el reporte: {e}")
    finally:
        connection.close()

# Función para obtener los reportes
def get_reports():
    connection = connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM reportes ORDER BY timestamp DESC")
            return cursor.fetchall()
    finally:
        connection.close()
# Token de Mapbox (reemplázalo por tu propio token)
MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiaGlyYW0wNjAyMjAiLCJhIjoiY204cGx2MG53MGM2eDJqb21ud2h1enIwOCJ9.nd8HgkDj3SEJlr-oQY8ufg'

app = Flask(__name__, static_folder='static')

# Ruta principal que muestra la página inicial
@app.route('/')
def index():
    return render_template('index.html')


# Ruta principal que muestra la página inicial
@app.route('/<ruta_id>/gif')
def gif(ruta_id):
    url = "https://raw.githubusercontent.com/Yael200206/YOVOY/main/Rutas.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        rutas_data = response.json()
    else:
        rutas_data = {"routes": []}  # Aseguramos que siempre haya una lista

    # Buscar la ruta con el ID dado
    ruta_seleccionada = next((ruta for ruta in rutas_data["routes"] if ruta["id"] == ruta_id), None)

    if ruta_seleccionada is None:
        return "Ruta no encontrada", 404

    # Extraer origen y destino desde el "name"
    nombre_ruta = ruta_seleccionada["name"]
    partes = nombre_ruta.split(" - ", 1)  # Dividir por el guion y espacio
    
    origen = partes[0].split(" ", 1)[1] if len(partes) > 1 else "Desconocido"
    destino = partes[1] if len(partes) > 1 else "Desconocido"

    # Agregar origen y destino al diccionario de la ruta
    ruta_seleccionada["origen"] = origen
    ruta_seleccionada["destino"] = destino

    return render_template('gif.html', ruta=ruta_seleccionada)


# Ruta para mostrar la página de la casa
@app.route('/house')
def home():
    return render_template('house.html')


@app.route('/rutas')
def rutas():
    # Obtener el archivo JSON desde la URL de GitHub
    url = "https://raw.githubusercontent.com/Yael200206/YOVOY/main/Rutas.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Si la respuesta es exitosa (200), cargar el contenido JSON
        rutas_data = response.json()
    else:
        # Si no se obtiene el JSON correctamente, devolver un diccionario vacío
        rutas_data = {}
    print(rutas_data)

    # Pasar el diccionario con los datos a la plantilla
    return render_template('rutas.html', rutas=rutas_data)


@app.route('/reportes')
def reportes():
    reports = get_reports()  # Obtiene los reportes desde la base de datos
    return render_template('reportes.html', reports=reports)


# Verifica si la extensión del archivo es válida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def insert_report(bus_id, description, category, image_filename=None):
    """Inserta un reporte con o sin imagen en la base de datos."""
    connection = connect()
    try:
        with connection.cursor() as cursor:
            if image_filename:
                sql = """
                INSERT INTO reportes (bus_id, description, category, image)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (bus_id, description, category, image_filename))
            else:
                sql = """
                INSERT INTO reportes (bus_id, description, category)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (bus_id, description, category))

            connection.commit()
    finally:
        connection.close()
 
# Ruta para subir reportes
@app.route('/upload', methods=['GET', 'POST'])
def upload_report():
    if request.method == 'POST':
        bus_id = request.form['bus_id']
        description = request.form['description']
        category = request.form['category']

        image_filename = None

        # Verifica si hay imagen seleccionada
        if 'image' in request.files:
            file = request.files['image']

            # Si hay archivo y es válido, lo sube
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_filename = f"uploads/{filename}"  # Ruta relativa

            # Si el archivo no es válido
            elif file.filename != '':
                flash('Formato de archivo no permitido', 'error')
                return redirect(url_for('upload_report'))

        # Inserta el reporte, con o sin imagen
        insert_report(bus_id, description, category, image_filename)
        flash('Reporte subido exitosamente', 'success')
        return redirect(url_for('reportes'))

    return render_template('re´prtes.html')
@app.route('/config')
def config():
    return render_template('config.html')

@app.route('/recargas')
def puntos_recarga():
    url = 'https://raw.githubusercontent.com/Yael200206/YOVOY/main/app/static/puntosRecarga.json'  # Enlace raw del archivo JSON
    
    try:
        # Realizamos una solicitud GET a la URL
        response = requests.get(url)
        
        # Verificamos si la solicitud fue exitosa
        if response.status_code == 200:
            data = response.json()  # Parseamos el JSON de la respuesta
        else:
            return jsonify({"error": f"Error al obtener el archivo JSON: {response.status_code}"}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error en la solicitud: {str(e)}"}), 500
    
    return render_template('recargas.html', puntos=data)
@app.route('/api/puntos_recarga')
def api_puntos_recarga():
    url = 'https://raw.githubusercontent.com/Yael200206/YOVOY/main/app/static/puntosRecarga.json'  # Enlace raw del archivo JSON
    
    try:
        # Realizamos una solicitud GET a la URL
        response = requests.get(url)
        
        # Verificamos si la solicitud fue exitosa
        if response.status_code == 200:
            data = response.json()  # Parseamos el JSON de la respuesta
        else:
            return jsonify({"error": f"Error al obtener el archivo JSON: {response.status_code}"}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error en la solicitud: {str(e)}"}), 500
    
    return jsonify(data)

# Ruta para la página de búsqueda de rutas
@app.route('/buscar_rutas', methods=['GET'])
def buscar_rutas():
    destination = request.args.get('destination')
    if destination:
        origin = "José Ventura López 222"  # Dirección origen fija

        

            # Pasar las rutas y el destino a la plantilla para su visualización
        return render_template('buscarRutas.html', destination=destination, origin=origin)


    else:
        return "No se especificó un destino", 400



if __name__ == '__main__':
    app.run(debug=True)
app.secret_key = 'Pitulillo$1'