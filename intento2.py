import requests

# URL del servidor al que deseas hacer la solicitud
url_login = 'https://elrutero.com.mx/login'  # Cambia la URL a la de tu servidor
url_protected = 'https://elrutero.com.mx/protected'  # Cambia esta URL al recurso al que quieres acceder

# Datos de autenticación (si es necesario)
payload = {
    'username': 'tu_usuario',  # Reemplaza con tu nombre de usuario
    'password': 'tu_contraseña',  # Reemplaza con tu contraseña
}

# Crea una sesión para manejar cookies y mantener la sesión activa
session = requests.Session()

# Establece el User-Agent para simular una solicitud de navegador
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}

# Enviar una solicitud POST para iniciar sesión y obtener la cookie de sesión
response_login = session.post(url_login, data=payload, headers=headers)

# Verifica si el inicio de sesión fue exitoso
if response_login.status_code == 200:
    print("Inicio de sesión exitoso.")
else:
    print(f"Error en el inicio de sesión: {response_login.status_code}")
    exit()

# Ahora que estamos autenticados, intentamos acceder a la página protegida
response_protected = session.get(url_protected, headers=headers)

# Verifica el código de estado de la respuesta
if response_protected.status_code == 200:
    print("Acceso a la página protegida exitoso.")
    # Imprimir el contenido de la página protegida
    print(response_protected.text)
elif response_protected.status_code == 419:
    print("Error 419: La sesión ha expirado. Intenta iniciar sesión nuevamente.")
else:
    print(f"Error al obtener la página protegida. Código de estado: {response_protected.status_code}")
