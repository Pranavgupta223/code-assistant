from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
def ask(request: QueryRequest):
    retrieved_chunks = search_query(request.query)
    answer = generate_answer(request.query, retrieved_chunks)

    return {
        "answer": answer
    }