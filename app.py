from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from ingest import load_code_files, chunk_code
from retriever import create_vector_store, search_query
from llm import generate_answer


# -----------------------------
# App Initialization
# -----------------------------
app = FastAPI()

templates = Jinja2Templates(directory="templates")


# -----------------------------
# Load & Prepare Data (Startup)
# -----------------------------
index = None
texts = None

# -----------------------------
# Request Schema
# -----------------------------
class QueryRequest(BaseModel):
    query: str


# -----------------------------
# Routes
# -----------------------------

@app.get("/")
def home():
    return {"message": "AI Code Assistant Running 🚀"}


@app.post("/ask")
def ask_question(request: QueryRequest):
    if index is None:
        return {"error": "Model still loading, try again in few seconds"}

    query = request.query

    retrieved_chunks = search_query(query, index, texts)
    answer = generate_answer(query, retrieved_chunks)

    return {
        "query": query,
        "answer": answer,
        "retrieved_chunks": retrieved_chunks
    }


@app.get("/ui", response_class=HTMLResponse)
def ui(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"request": request}
    )

@app.on_event("startup")
def load_model():
    global index, texts

    files = load_code_files("data/sample_project")
    chunks = chunk_code(files)
    index, texts = create_vector_store(chunks)

    print("Model loaded successfully")