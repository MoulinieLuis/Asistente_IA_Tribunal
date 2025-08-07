import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

modelo = SentenceTransformer("all-MiniLM-L6-v2")

# Simulación de fragmentos
fragmentos = [
    "Para cambiar días de descanso, vaya a Configuración > RRHH > Empleados.",
    "Los reportes de nómina se generan desde el módulo de Nómina.",
    "Para crear un nuevo usuario, accede al panel de Administración > Usuarios.",
]

vectores = modelo.encode(fragmentos)

# Crear índice FAISS
index = faiss.IndexFlatL2(vectores.shape[1])
index.add(vectores.astype(np.float32))  # <--- Aquí estaba mal antes

def buscar_fragmento_relacionado(pregunta: str) -> str:
    vector_pregunta = modelo.encode([pregunta])
    distancias, indices = index.search(vector_pregunta.astype(np.float32), k=1)  # <--- Corregido
    indice_mas_cercano = indices[0][0]
    return fragmentos[indice_mas_cercano]
