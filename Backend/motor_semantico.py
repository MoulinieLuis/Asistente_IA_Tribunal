import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# 🚀 Carga modelo de embeddings
modelo_embeddings = SentenceTransformer("all-MiniLM-L6-v2")

# Evita regenerar embeddings si ya existe índice
def cargar_o_crear_indice(ruta, textos):
    dim = 384  # all-MiniLM-L6-v2 dimensión fija
    index = faiss.IndexFlatL2(dim)
    embeddings = modelo_embeddings.encode(textos)

    index.add(np.array(embeddings).astype("float32"))
    return index, textos

# 🔽 Buscar solo 3 fragmentos
def buscar_fragmentos_relacionados(pregunta: str, index, textos, k=3):
    embedding_pregunta = modelo_embeddings.encode([pregunta])
    D, I = index.search(np.array(embedding_pregunta).astype("float32"), k)
    
    fragmentos = []
    for idx in I[0]:
        if idx < len(textos):
            # 🔽 Limitar longitud de cada fragmento
            fragmentos.append(textos[idx][:500])  
    return fragmentos
