# functions/project_naming.py

from openai import OpenAI, OpenAIError
from config import MODEL_NAME

def suggest_project_names(client: OpenAI, project_description: str) -> str:
    try:
        user_input = (
            f"Suggest 5 creative and relevant names for the following project: '{project_description}'. "
            "Ensure the names are unique and reflect the project's objectives."
        )
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that generates creative and relevant project names based on descriptions and objectives.",
                },
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
        )
        
        message = response.choices[0].message.content
        return message

    except OpenAIError as e:
        return f"API request failed: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

