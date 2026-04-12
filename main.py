from ingest import load_code_files, chunk_code
from retriever import create_vector_store, search_query
from llm import generate_answer


files = load_code_files("data/sample_project")
chunks = chunk_code(files)
index, texts = create_vector_store(chunks)


while True:
    query = input("\nAsk your question (type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    retrieved_chunks = search_query(query, index, texts)

    answer = generate_answer(query, retrieved_chunks)

    print("\nFinal Answer:\n", answer)