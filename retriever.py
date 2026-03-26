import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("storage/index.faiss")

with open ("storage/metadata.json", "r") as f:
    metadata = json.load(f)

def retrieve(query, k=3):
    
    query_vector = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vector, k)
    
    results = []

    for idx in indices[0]:
        if idx != -1:
            results.append(metadata[idx])

    return results 
