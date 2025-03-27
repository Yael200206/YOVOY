import requests
import json
import time
from tqdm import tqdm  # Barra de progreso

# Función para obtener las coordenadas usando Mapbox
def obtener_coordenadas_mapbox(direccion, api_key):
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{direccion}.json?access_token={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if 'features' in data and data['features']:
        lat = data['features'][0]['geometry']['coordinates'][1]
        lon = data['features'][0]['geometry']['coordinates'][0]
        return lat, lon
    else:
        print(f"No se encontraron resultados para '{direccion}'")
        return None, None

# Lista de direcciones
direcciones = [
    "Terminal Vicente Guerrero",
    "Avenida De Los Maestros, 4202",
    "Bodega Aurrera",
    "Avenida Siglo Xxi, 3832",
    "Avenida Siglo Xxi, 3306",
    "Dolores Del Río, 116",
    "Corsel 134(Inta",
    "Prolongación Paseo De La Asunción, 2",
    "Prolongación Paseo De La Asunción, 212",
    "Prolongación Paseo De La Asunción, Sn(Ct)",
    "Quinta Avenida, 813",
    "República De Brasil, 609",
    "Central Camionera",
    "Convencion 1914 Sur, 308",
    "Avenida José Maria Chávez, 1217",
    "Avenida José Maria Chávez, 1014",
    "Avenida José Maria Chávez, 710",
    "Jose Maria Chavez, 524",
    "5 De Mayo, 401",
    "5 De Mayo, 552-558",
    "Petróleos Mexicanos, 215",
    "General Miguel Barragán, 1224",
    "A Zacatecas, 1711",
    "Boulevard A Zacatecas, 1404(1402)",
    "Héroe De Nacozari Norte, 3005",
    "A Zacatecas, Km5",
    "Carretera Federal 45 845",
    "Centro Comercial Altaria",
    "A Zacatecas, 309",
    "Aguascalientes - San Francisco De Los Romo, 273",
    "Carretera Panamericana, 18",
    "Venustiano Carranza, 101",
    "Avenida Margaritas, 201a",
    "Antiguo Camino A Zacatecas, 500",
    "Terminal Margaritas"
]

# Clave API de Mapbox (reemplaza con la tuya)
api_key = "pk.eyJ1IjoiaGlyYW0wNjAyMjAiLCJhIjoiY204cGx2MG53MGM2eDJqb21ud2h1enIwOCJ9.nd8HgkDj3SEJlr-oQY8ufg"

# Archivo donde se guardarán las coordenadas
archivo_salida = "01vicente.json"

# Cargar datos previos si existen
try:
    with open(archivo_salida, 'r') as f:
        resultados = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    resultados = []

# Convertir a diccionario para evitar duplicados
direcciones_guardadas = {r["direccion"]: (r["latitud"], r["longitud"]) for r in resultados}

# Procesar cada dirección con una barra de progreso
with tqdm(total=len(direcciones), desc="Obteniendo coordenadas") as pbar:
    for direccion in direcciones:
        if direccion in direcciones_guardadas:
            print(f"{direccion} ya está en el archivo. Saltando...")
        else:
            lat, lon = obtener_coordenadas_mapbox(direccion, api_key)
            if lat is not None and lon is not None:
                resultado = {"direccion": direccion, "latitud": lat, "longitud": lon}
                resultados.append(resultado)
                # Guardar en el archivo inmediatamente
                with open(archivo_salida, 'w') as f:
                    json.dump(resultados, f, indent=4)
            time.sleep(1)  # Pequeña pausa para evitar bloqueos de API
        pbar.update(1)

print(f"Las coordenadas se han guardado en {archivo_salida}.")