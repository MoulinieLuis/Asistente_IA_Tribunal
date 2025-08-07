import requests

HUGGINGFACE_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"

HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
    "Content-Type": "application/json"
}

def preguntar_ia(prompt: str) -> str:
    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={"inputs": prompt},
            timeout=10  # opcional para evitar bloqueos prolongados
        )
    except requests.exceptions.ConnectionError:
        return "[ERROR] No se pudo conectar con la API de Hugging Face. Verifica tu conexión."
    except requests.exceptions.Timeout:
        return "[ERROR] La petición a la IA tardó demasiado tiempo."

    if response.status_code != 200:
        return f"[ERROR] No se pudo obtener respuesta de la IA: {response.text}"

    data = response.json()

    try:
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict) and "generated_text" in data[0]:
            return data[0]["generated_text"]
        elif isinstance(data, dict) and "generated_text" in data:
            return data["generated_text"]
        else:
            return "No se pudo interpretar la respuesta de la IA."
    except Exception:
        return "No se pudo interpretar la respuesta de la IA."
