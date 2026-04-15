import os
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_answer(query, retrieved_chunks):
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are a helpful AI code assistant.

Use the provided code context to answer the user's question.

Code Context:
{context}

User Question:
{query}

Answer clearly and give examples if needed.
"""

    response = model.generate_content(prompt)
    return response.text