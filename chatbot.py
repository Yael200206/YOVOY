import requests
import json
from tqdm import tqdm  

def obtener_coordenadas_mapbox(direccion, api_key):
    direccion_completa = f"{direccion}, Aguascalientes, México"
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{direccion_completa}.json?access_token={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if 'features' in data and data['features']:
            lat = data['features'][0]['geometry']['coordinates'][1]
            lon = data['features'][0]['geometry']['coordinates'][0]

            # Verificar si la dirección realmente es de Aguascalientes
            if 'context' in data['features'][0]:
                for elemento in data['features'][0]['context']:
                    if "Aguascalientes" in elemento['text']:
                        return lat, lon  # Solo devuelve si está en Aguascalientes
                print(f"Ignorada (fuera de Aguascalientes): {direccion}")
                return None, None
            else:
                return lat, lon
        else:
            print(f"No se encontraron resultados para '{direccion}'")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud para '{direccion}': {e}")
        return None, None
    except KeyError:
        print(f"Error en la respuesta para '{direccion}': No se encontró la clave esperada.")
        return None, None

# Cargar direcciones
with open('direcciones.json', 'r') as f:
    direcciones_json = json.load(f)

api_key = "pk.eyJ1IjoiaGlyYW0wNjAyMjAiLCJhIjoiY204cGx2MG53MGM2eDJqb21ud2h1enIwOCJ9.nd8HgkDj3SEJlr-oQY8ufg"

with open('direcciones_con_coordenadas.json', 'w') as f:
    f.write('[')
    primera = True

    for direccion in tqdm(direcciones_json["direcciones"], desc="Obteniendo coordenadas", unit="direccion"):
        lat, lon = obtener_coordenadas_mapbox(direccion, api_key)
        if lat is not None and lon is not None:
            resultado = {"direccion": direccion, "latitud": lat, "longitud": lon}

            if not primera:
                f.write(',\n')
            json.dump(resultado, f, indent=4)
            primera = False

    f.write('\n]')

print("Resultados guardados en 'direcciones_con_coordenadas.json'.")
