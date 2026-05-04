from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from ingest import load_code_files, chunk_code
from retriever import create_vector_store, search_query
from llm import generate_answer

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load project once
files = load_code_files("data/sample_project")
chunks = chunk_code(files)
index, texts = create_vector_store(chunks)


class QueryRequest(BaseModel):
    query: str


@app.get("/ui")
def ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/ask")
def ask(request: QueryRequest):
    try:
        retrieved_chunks = search_query(request.query, index, texts)

        if not retrieved_chunks:
            return {"answer": "No relevant code found."}

        answer = generate_answer(request.query, retrieved_chunks)

        if not answer:
            return {"answer": "Model did not return a response."}

        return {"answer": answer}

    except Exception as e:
        return {"answer": f"Server error: {str(e)}"}