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

def load_system():
    global index, texts

    if index is None:
        files = load_code_files("data/sample_project")
        chunks = chunk_code(files)
        index, texts = create_vector_store(chunks)

        
@app.post("/ask")
def ask_question(request: QueryRequest):
    load_system()

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