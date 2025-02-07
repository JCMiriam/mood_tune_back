import pandas as pd
import torch
import numpy as np
import faiss  # 🔥 Importar FAISS para búsquedas rápidas
from sentence_transformers import SentenceTransformer

# 📌 Ruta del archivo de embeddings generados con RoBERTa
EMBEDDINGS_FILE = r"C:\Users\solan\mood_tune_back\src\models\embeddings_roberta2.pkl"

# 📌 Cargar el dataset con los embeddings
df = pd.read_pickle(EMBEDDINGS_FILE)

# 📌 Convertir embeddings a NumPy arrays de tipo float32 (para FAISS)
df['embedding'] = df['embedding'].apply(lambda x: np.array(x, dtype=np.float32))

# 📌 Crear un índice FAISS para búsqueda rápida (usamos IndexFlatIP para máxima precisión)
embeddings = np.stack(df["embedding"].values)  # Convertir embeddings a matriz
index = faiss.IndexFlatIP(embeddings.shape[1])  # Índice con similitud coseno
index.add(embeddings)  # Cargar los embeddings en FAISS

# 📌 Cargar modelo RoBERTa en GPU si está disponible
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer('all-roberta-large-v1', device=device)

# 📌 Almacenar objetos en un diccionario para fácil acceso desde otros archivos
model_data = {
    "df": df,
    "index": index,
    "model": model
}
