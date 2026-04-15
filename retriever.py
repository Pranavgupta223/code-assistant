def create_vector_store(chunks):
    texts = [
        f"File: {chunk['file_name']}\nCode:\n{chunk['chunk']}"
        for chunk in chunks
    ]

    return None, texts


def search_query(query, index, texts):
    query = query.lower()

    matched = []

    for text in texts:
        if any(word in text.lower() for word in query.split()):
            matched.append(text)

    if not matched:
        matched = texts[:2]

    return matched[:2]