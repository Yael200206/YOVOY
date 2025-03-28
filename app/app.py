from flask import Flask, render_template, request, jsonify
import requests
import json
import os

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
def resportes():
    return render_template('reportes.html')

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
