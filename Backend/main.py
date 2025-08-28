from fastapi import FastAPI
from ia_connector import consultar_modelo
from motor_semantico import cargar_o_crear_indice, buscar_fragmentos_relacionados

app = FastAPI()

# 🚀 Simulación de base de datos de manual
manual_textos = [
    "Este es un ejemplo de contenido del manual. Explica cómo encender el dispositivo.",
    "Este fragmento habla sobre seguridad en el uso del dispositivo.",
    "Este fragmento explica cómo solucionar errores comunes."
]

indice, textos = cargar_o_crear_indice("ruta_indice", manual_textos)

@app.get("/preguntar/")
async def preguntar(pregunta: str):
    fragmentos = buscar_fragmentos_relacionados(pregunta, indice, textos)

    contexto = "\n\n".join(fragmentos)
    prompt = f"""
Responde la siguiente pregunta basándote **exclusivamente** en el manual proporcionado.
Si no está en el manual, responde: 'No encontré esa información en el manual.'

Manual (fragmentos relevantes):
{contexto}

Pregunta: {pregunta}
Respuesta:
"""
    respuesta = consultar_modelo(prompt)
    return {"respuesta": respuesta}
