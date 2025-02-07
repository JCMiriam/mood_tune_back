import os
import sys
import importlib.util
import subprocess
import pandas as pd
import torch
import numpy as np


# 📌 Ruta del archivo de embeddings
EMBEDDINGS_FILE = r"C:\Users\solan\mood_tune_back\src\models\embeddings_roberta2.pkl" # RUTA DONDE ESTÉN METIDOS LOS EMBEDDINGS 

# 📌 Cargar el dataset con los embeddings
print("🔄 Cargando datos de embeddings...")
df = pd.read_pickle(EMBEDDINGS_FILE)

# 📌 Convertir embeddings a NumPy array si están en listas
if isinstance(df['embedding'][0], list):
    df['embedding'] = df['embedding'].apply(lambda x: np.array(x))

embeddings_matrix = np.vstack(df['embedding'].values).astype('float32')

# 📌 Crear índice FAISS
dimension = embeddings_matrix.shape[1]
index = faiss.IndexFlatL2(dimension)  
index.add(embeddings_matrix)

print("✅ FAISS index creado.")

# 📌 Cargar modelo RoBERTa en GPU si está disponible
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"⚡ Usando: {device.upper()}")

model = SentenceTransformer('all-roberta-large-v1', device=device)

# 📌 Guardar los objetos en un diccionario
model_data = {
    "df": df,
    "index": index,
    "model": model
}

print("✅ Modelo y datos listos para usar.")
