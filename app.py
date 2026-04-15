=from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from retriever import search_query
from llm import generate_answer

app = FastAPI()

templates = Jinja2Templates(directory="templates")


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
    retrieved_chunks = search_query(request.query)
    answer = generate_answer(request.query, retrieved_chunks)

    return {
        "answer": answer
    }