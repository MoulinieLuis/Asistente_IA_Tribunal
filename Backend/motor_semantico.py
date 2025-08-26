# motor_semantico.py

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import fitz  # PyMuPDF para leer PDFs
import os

# ======================
# Configuración general
# ======================
MODELO = SentenceTransformer("all-MiniLM-L6-v2")
DATA_DIR = "data"
EMBEDDINGS_FILE = "embeddings/manual_embeddings.faiss"
FRAGMENTS_FILE = "embeddings/manual_fragments.txt"


# ======================
# Funciones principales
# ======================

def procesar_manuales_y_generar_embeddings():
    """
    Lee todos los PDFs en la carpeta 'data', extrae el texto, lo divide en fragmentos
    y genera embeddings. Guarda los resultados en archivos FAISS y TXT.
    """
    fragmentos = []
    print("📄 Procesando manuales...")

    # Crear carpeta embeddings si no existe
    os.makedirs("embeddings", exist_ok=True)

    # Recorrer PDFs en la carpeta "data"
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".pdf"):
            filepath = os.path.join(DATA_DIR, filename)
            try:
                documento = fitz.open(filepath)
                texto_completo = ""
                for page in documento:
                    texto_completo += page.get_text("text")

                # Dividir en fragmentos (párrafos separados por doble salto de línea)
                nuevos_fragmentos = [p.strip() for p in texto_completo.split('\n\n') if p.strip()]
                fragmentos.extend(nuevos_fragmentos)
                print(f"   ✅ {filename}: {len(nuevos_fragmentos)} fragmentos extraídos")

            except Exception as e:
                print(f"   ⚠️ Error al procesar {filename}: {e}")

    if not fragmentos:
        print("⚠️ No se encontraron fragmentos para procesar.")
        return None, None

    # Codificar todos los fragmentos
    print("⚙️ Generando embeddings...")
    vectores = MODELO.encode(fragmentos, show_progress_bar=True)

    # Crear índice FAISS
    dimension = vectores.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectores.astype(np.float32))

    # Guardar embeddings e índice FAISS
    faiss.write_index(index, EMBEDDINGS_FILE)

    # Guardar fragmentos en archivo
    with open(FRAGMENTS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(fragmentos))

    print("✅ Procesamiento completo. Embeddings guardados.")
    return index, fragmentos


def cargar_o_generar_embeddings():
    """
    Carga embeddings y fragmentos desde disco si existen,
    de lo contrario, procesa los manuales y los genera.
    """
    if os.path.exists(EMBEDDINGS_FILE) and os.path.exists(FRAGMENTS_FILE):
        print("📂 Cargando embeddings y fragmentos desde archivos...")
        index = faiss.read_index(EMBEDDINGS_FILE)
        with open(FRAGMENTS_FILE, 'r', encoding='utf-8') as f:
            fragmentos = f.read().split('\n\n')
        print(f"✅ {len(fragmentos)} fragmentos cargados.")
        return index, fragmentos
    else:
        return procesar_manuales_y_generar_embeddings()


def buscar_fragmentos_relacionados(pregunta: str, k: int = 5) -> list[str]:
    """
    Busca los fragmentos más relevantes para una pregunta dada.
    Retorna los 'k' fragmentos más similares.
    """
    if index is None or fragmentos is None:
        print("⚠️ Error: índice o fragmentos no cargados.")
        return []

    # Codificar la pregunta
    vector_pregunta = MODELO.encode([pregunta])
    distancias, indices = index.search(vector_pregunta.astype(np.float32), k=k)

    # Recuperar fragmentos relevantes
    resultados = [fragmentos[i] for i in indices[0] if i < len(fragmentos)]
    return resultados


# ======================
# Inicialización global
# ======================
index, fragmentos = cargar_o_generar_embeddings()

# Alias más intuitivo para usar desde main.py
buscar_fragmento_relacionado = buscar_fragmentos_relacionados