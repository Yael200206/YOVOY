from flask import Flask, render_template, request, jsonify
import requests
import json
import os

# Token de Mapbox (reemplázalo por tu propio token)
MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiaGlyYW0wNjAyMjAiLCJhIjoiY204cGx2MG53MGM2eDJqb21ud2h1enIwOCJ9.nd8HgkDj3SEJlr-oQY8ufg'

app = Flask(__name__)

# Ruta principal que muestra la página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para mostrar la página de la casa
@app.route('/house')
def home():
    return render_template('house.html')

# Ruta para mostrar la página de la casa
@app.route('/rutas')
def rutas():
    return render_template('rutas.html')

@app.route('/reportes')
def resportes():
    return render_template('reportes.html')
@app.route('/recargas')
def puntos_recarga():
    file_path = r'C:\Users\XOCEA\OneDrive\Documentos\YOVOY\app\static\puntosRecarga.json'
    if not os.path.exists(file_path):
        return jsonify({"error": "Archivo puntosRecarga.json no encontrado"}), 404
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return render_template('recargas.html', puntos=data)

@app.route('/api/puntos_recarga')
def api_puntos_recarga():
    file_path = os.path.join('static', 'puntosRecarga.json')
    file_path=r"C:\Users\XOCEA\OneDrive\Documentos\YOVOY\app\static\puntosRecarga.json"
    if not os.path.exists(file_path):
        return jsonify({"error": "Archivo puntosRecarga.json no encontrado"}), 404

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
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
