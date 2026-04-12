from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


model = SentenceTransformer("all-MiniLM-L6-v2")

def create_vector_store(chunks):
    texts = [
        f"File: {chunk['file_name']}\nCode:\n{chunk['chunk']}"
        for chunk in chunks
    ]

    embeddings = model.encode(texts)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))

    return index, texts

def search_query(query, index, texts, top_k=2):
    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding).astype("float32"),
        top_k
    )

    results = []

    for i in indices[0]:
        results.append(texts[i])

    return results