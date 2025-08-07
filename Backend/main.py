from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from motor_semantico import buscar_fragmento_relacionado
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
    contexto = buscar_fragmento_relacionado(pregunta)

    prompt = f"""
    Usa el siguiente fragmento del manual para responder a la pregunta del usuario.

    Fragmento del manual:
    {contexto}

    Pregunta del usuario:
    {pregunta}

    Respuesta clara y concisa:
    """

    respuesta = preguntar_ia(prompt)

    # Si es error, devolverlo con un status adecuado (podrías hacer try/except con HTTPException)
    if respuesta.startswith("[ERROR]"):
        return {"error": respuesta}

    return {
        "pregunta": pregunta,
        "fragmento_relacionado": contexto,
        "respuesta": respuesta
    }


#Final comment