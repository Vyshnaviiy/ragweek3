
import ollama


def generate_response(prompt):

    try:

        response = ollama.chat(
            model="phi3",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:

        return f"Ollama Error: {str(e)}"

