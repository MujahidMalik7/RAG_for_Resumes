import os
import json 
import numpy as np
import faiss
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

directory = "data/resumes/"

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
    
        for page in reader.pages:
            text += page.extract_text()
        
    if text.strip() == "":
        return None
    return text

def chunk_text(text, chunk_size = 1000, overlap = 250):
    chunks = []
    start = 0
    while start<len(text):
        chunks.append(text[start:start+chunk_size])
        start += chunk_size - overlap
    return chunks

model = SentenceTransformer('all-MiniLM-L6-v2')
all_chunks = []
metadata = []

for filename in os.listdir(directory):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(directory, filename)

        #extract text
        text = extract_text_from_pdf(pdf_path)

        if text:
            chunks = chunk_text(text)
            for i,chunk in enumerate(chunks):
                all_chunks.append(chunk)
                metadata.append({"source": filename, "chunk_id": i, "text": chunk})
                print(f"Chunk {i+1}: {len(chunk)} characters")

embeddings = model.encode(all_chunks).astype("float32")

index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, "storage/index.faiss")
with open("storage/metadata.json", "w") as f:
    json.dump(metadata, f)

print(f"Total chunks: {len(all_chunks)}")
print("Index and metadata saved to storage/")