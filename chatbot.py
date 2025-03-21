import requests
import json

# Configuración de la API de Ollama
OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Ajusta la URL según tu configuración de Ollama

def get_ollama_response(prompt):
    data = {
        "model": "llama3.2",  # Usa el modelo Llama 3.2
        "prompt": prompt,
        "stream": False  # Desactiva el streaming para obtener una respuesta completa
    }
    
    response = requests.post(OLLAMA_API_URL, json=data)
    
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"Error: {response.status_code}, {response.text}"

def main():
    print("Bienvenido al chatbot. Escribe 'salir' para terminar.")
    
    while True:
        prompt = input("Tú: ")
        
        if prompt.lower() == "salir":
            print("Chatbot: ¡Hasta luego!")
            break
        
        # Obtén la respuesta del modelo Llama 3.2
        response = get_ollama_response(prompt)
        
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()