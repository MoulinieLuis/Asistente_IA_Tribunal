import requests  # Importa la librería requests para hacer peticiones HTTP

# Definición de la función que envía una pregunta a la IA local
def preguntar_ia(prompt: str) -> str:
    try:
        # Dirección del servidor local de la IA (Ollama en este caso)
        url = "http://localhost:11434/api/generate"
        
        # Cuerpo de la petición con el modelo a usar y el prompt del usuario
        payload = {
            "model": "mistral",  # Nombre del modelo de IA cargado en Ollama
            "prompt": prompt     # Texto de entrada que envía el usuario
        }
        
        # Enviar la petición POST al servidor de IA con el payload en formato JSON
        # stream=True permite recibir la respuesta poco a poco (en "chunks")
        response = requests.post(url, json=payload, stream=True)

        respuesta = ""  # Variable para ir acumulando el texto de la respuesta

        # Itera línea por línea de la respuesta transmitida por streaming
        for line in response.iter_lines():
            if line:  # Si la línea no está vacía
                data = line.decode("utf-8")  # Decodifica los bytes a string
                import json  # Importa json para convertir el string a objeto Python
                obj = json.loads(data)  # Convierte la línea a un diccionario
                
                # Si la línea contiene una parte de la respuesta de la IA, la agrega
                if "response" in obj:
                    respuesta += obj["response"]

        # Retorna la respuesta completa quitando espacios en blanco extras
        return respuesta.strip()

    # Manejo de errores en caso de que la conexión con la IA falle
    except Exception as e:
        return f"[ERROR] No se pudo conectar con la IA local: {e}"
    
