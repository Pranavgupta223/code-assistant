import os
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_answer(query, retrieved_chunks):
    try:
        context = "\n\n".join([str(c) for c in retrieved_chunks])

        prompt = f"""
You are a helpful AI code assistant.

Code Context:
{context}

User Question:
{query}
"""

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"LLM error: {str(e)}"