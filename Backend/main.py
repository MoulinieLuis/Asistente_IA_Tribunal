# main.py

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from motor_semantico import buscar_fragmentos_relacionados
from ia_connector import preguntar_ia

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/preguntar")
def preguntar(pregunta: str = Query(..., description="Pregunta del usuario")):
    # Ahora buscamos varios fragmentos
    contextos = buscar_fragmentos_relacionados(pregunta)
    
    # Unir los fragmentos en una sola cadena para el prompt
    contexto_completo = "\n\n---\n\n".join(contextos)

    prompt = f"""
    Usa los siguientes fragmentos del manual para responder a la pregunta del usuario.
    Todo texto generado como respuesta debe estar en idioma español 
    Combina la información de todos los fragmentos si es necesario, pero solo usa la información que se te proporciona.
    Si la pregunta no puede ser respondida con la información de los fragmentos, di que no tienes la información necesaria.

    Fragmentos del manual:
    {contexto_completo}

    Pregunta del usuario:
    {pregunta}

    Respuesta clara y concisa:
    """

    respuesta = preguntar_ia(prompt)

    if respuesta.startswith("[ERROR]"):
        return {"error": respuesta}

    return {
        "pregunta": pregunta,
        "fragmentos_relacionados": contextos, # Devolvemos todos los fragmentos
        "respuesta": respuesta
    }