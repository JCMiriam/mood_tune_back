import pandas as pd
import torch
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os
import pickle

# 📌 Ruta de los archivos
FAISS_INDEX_FILE = os.path.join(os.path.dirname(__file__), "lyrics_embeddings_faiss_IP.index")
EMBEDDINGS_FILE = os.path.join(os.path.dirname(__file__), "lyrics_embeddings_roberta3.pkl")

# 📌 Cargar FAISS (Índice de Embeddings)
if not os.path.exists(FAISS_INDEX_FILE):
    raise FileNotFoundError(f"❌ Error: No se encontró el archivo {FAISS_INDEX_FILE}")

try:
    index = faiss.read_index(FAISS_INDEX_FILE)
    print("✅ FAISS Index cargado correctamente.")
except Exception as e:
    raise RuntimeError(f"❌ Error al cargar el índice FAISS: {e}")

# 📌 Cargar modelo RoBERTa en GPU si está disponible
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"⚡ Usando: {device.upper()}")

model = SentenceTransformer('sentence-transformers/all-roberta-large-v1', device=device)

# 📌 Cargar el DataFrame con las canciones
df = None  # Inicialmente None

if os.path.exists(EMBEDDINGS_FILE):
    try:
        df = pd.read_pickle(EMBEDDINGS_FILE)
        print("✅ DataFrame con embeddings cargado correctamente.")
    except Exception as e:
        print(f"❌ Error al cargar el DataFrame: {e}")

# 📌 Diccionario global con modelos y datos
model_data = {
    "index": index,
    "model": model,
    "df": df  # Asegurarse de que df no sea None
}
