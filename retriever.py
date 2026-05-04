def create_vector_store(chunks):
    texts = [
        f"File: {chunk['file_name']}\nCode:\n{chunk['chunk']}"
        for chunk in chunks
    ]

    return None, texts


def search_query(query, index, texts):
    query_words = query.lower().split()

    scored = []

    for text in texts:
        score = sum(word in text.lower() for word in query_words)
        scored.append((score, text))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [text for score, text in scored[:3] if score > 0]