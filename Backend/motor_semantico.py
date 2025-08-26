# motor_semantico.py

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import fitz  # PyMuPDF library to read PDFs
import os

# Define the model and paths
modelo = SentenceTransformer("all-MiniLM-L6-v2")
DATA_DIR = "data"
EMBEDDINGS_FILE = "embeddings/manual_embeddings.faiss"
FRAGMENTS_FILE = "embeddings/manual_fragments.txt"

def procesar_manuales_y_generar_embeddings():
    """
    Lee todos los PDFs en la carpeta 'data', extrae el texto, lo divide en fragmentos
    y genera embeddings. Guarda los resultados en archivos.
    """
    fragmentos = []
    print("Procesando manuales...")

    # Asegurarse de que la carpeta de embeddings existe
    os.makedirs("embeddings", exist_ok=True)

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".pdf"):
            filepath = os.path.join(DATA_DIR, filename)
            try:
                documento = fitz.open(filepath)
                texto_completo = ""
                for page in documento:
                    texto_completo += page.get_text()

                # Dividir el texto en fragmentos. Un buen tamaño es entre 200 y 500 tokens.
                # Aquí lo dividiremos por párrafos (dos saltos de línea).
                nuevos_fragmentos = [p.strip() for p in texto_completo.split('\n\n') if p.strip()]
                fragmentos.extend(nuevos_fragmentos)
                print(f"   - Procesado: {filename} ({len(nuevos_fragmentos)} fragmentos)")

            except Exception as e:
                print(f"   - Error al procesar {filename}: {e}")

    if not fragmentos:
        print("No se encontraron fragmentos para procesar.")
        return None, None

    # Codificar todos los fragmentos
    print("Generando embeddings...")
    vectores = modelo.encode(fragmentos)

    # Crear y guardar el índice FAISS
    dimension = vectores.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectores.astype(np.float32))
    faiss.write_index(index, EMBEDDINGS_FILE)

    # Guardar los fragmentos en un archivo de texto
    with open(FRAGMENTS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(fragmentos))

    print("Procesamiento completo. Embeddings guardados.")
    return index, fragmentos

def cargar_o_generar_embeddings():
    """
    Carga los embeddings y fragmentos si existen, de lo contrario, los genera.
    """
    if os.path.exists(EMBEDDINGS_FILE) and os.path.exists(FRAGMENTS_FILE):
        print("Cargando embeddings y fragmentos desde archivos...")
        index = faiss.read_index(EMBEDDINGS_FILE)
        with open(FRAGMENTS_FILE, 'r', encoding='utf-8') as f:
            fragmentos = f.read().split('\n\n')
        print(f"Cargados {len(fragmentos)} fragmentos.")
        return index, fragmentos
    else:
        return procesar_manuales_y_generar_embeddings()

# Cargar o generar los embeddings al iniciar el módulo
index, fragmentos = cargar_o_generar_embeddings()

def buscar_fragmentos_relacionados(pregunta: str) -> list[str]:
    """
    Busca los fragmentos más relevantes para una pregunta dada.
    """
    if not index or not fragmentos:
        print("Error: El índice o los fragmentos no están cargados.")
        return []

    # Se busca por los 5 fragmentos más relevantes
    k = 5
    vector_pregunta = modelo.encode([pregunta])
    distancias, indices = index.search(vector_pregunta.astype(np.float32), k=k)
    
    resultados = [fragmentos[i] for i in indices[0]]
    return resultados

# Renombrar la función original para evitar conflictos,
# y hacer una llamada más clara desde main.py
buscar_fragmento_relacionado = buscar_fragmentos_relacionados