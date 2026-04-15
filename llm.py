import google.generativeai as genai

# Replace with your actual API key
client = genai.Client(api_key="AIzaSyCiL1-Ub9FFyjW3Ugv4fG102eLF_C7VnAk")

def generate_answer(query, context_chunks):
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are a helpful coding assistant.

Context:
{context}

Question:
{query}

Answer clearly:
"""

    try:
        # The new SDK uses client.models.generate_content
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"