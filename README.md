# 📚 Asistente Inteligente de Consulta Jurídica

## 📌 Descripción General
Este proyecto es un **asistente de consultas jurídicas** que combina:
1. **Un motor semántico** que busca información relevante en manuales oficiales del tribunal.
2. **Un modelo de IA** que genera respuestas completas y coherentes basadas en la información encontrada y en la pregunta del usuario.

El objetivo es proporcionar respuestas precisas y fundamentadas, integrando **conocimiento humano (manuales)** con **capacidad generativa de IA**.

---

## ⚙️ Funcionamiento General

1. **Recepción de la pregunta**
   - Un usuario envía su consulta a la API del proyecto.

2. **Búsqueda semántica**
   - El motor semántico analiza la pregunta y encuentra fragmentos relevantes en los manuales del tribunal.
   - Se utiliza **FAISS** como índice vectorial para buscar por similitud de significado.

3. **Generación de respuesta**
   - El contexto relevante (texto de manuales) y la pregunta se envían al **modelo de IA local**.
   - La IA combina la información encontrada con su propio conocimiento para generar una respuesta clara.

4. **Devolución al usuario**
   - La respuesta final se envía en formato JSON.

---

## 🧩 Componentes del Proyecto

- **`main.py`**  
  Contiene la API desarrollada en **FastAPI**.  
  Expone los endpoints para recibir consultas y devolver respuestas.

- **`semantic_engine.py`**  
  Módulo que maneja la búsqueda semántica usando FAISS y embeddings.

- **`ia_connector.py`**  
  Módulo que gestiona la conexión con el modelo de IA local.

- **`requirements.txt`**  
  Lista de dependencias necesarias para instalar el entorno.

- **`data/manuals`** *(opcional)*  
  Carpeta donde se almacenan los manuales del tribunal en texto plano para ser indexados.

---

## 🔗 Flujo de Relación entre Componentes

## 🖥️ Requerimientos del Sistema

- **Python** 3.9 o superior  
- **FastAPI** y **Uvicorn** para la API  
- **FAISS** para búsqueda semántica  
- **SentenceTransformers** para embeddings  
- **Transformers** y modelo local compatible  
- Sistema operativo: Linux, macOS o Windows  
- Al menos **8 GB de RAM** (recomendado 16 GB si el modelo es grande)  
- GPU con soporte CUDA *(opcional pero recomendado)*

---

## 📦 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/usuario/asistente-juridico.git
   cd asistente-juridico

2. **Crear entorno virtual**
  python -m venv venv
  source venv/bin/activate   # En Windows: venv\Scripts\activate

3. **Instalar dependencias**
  pip install -r requirements.txt


4. **Indexar manuales (opcional si ya existe el índice)**
  python semantic_engine.py --index


## 🚀 Ejecución

1. **Iniciar la API con recarga automática:**
  uvicorn main:app --reload


**La API de IA existe cuando se descaga la aplicación Ollama y se instala la IA "Mistral"**
  Puerto (localhost): http://127.0.0.1:8000


## 📋 Ejemplo de Uso

**Solicitud:**

curl -X POST "http://127.0.0.1:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "¿Cuál es el procedimiento para apelar una sentencia?"}'


**Respuesta:**

{
  "answer": "Según el manual del tribunal, el procedimiento para apelar...",
  "source": "Manual de Procedimientos, Capítulo 4"
}


## 👥 Colaboración

**Para contribuir:**

Crear una nueva rama.

Realizar cambios y pruebas.

Hacer un Pull Request con una descripción clara de las modificaciones.

![Arquitectura del Proyecto](img/arquitectura_proyecto_asistente.png)
