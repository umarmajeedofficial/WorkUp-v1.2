# functions/project_workflow.py

from openai import OpenAI, OpenAIError
from config import MODEL_NAME

def get_project_workflow(client: OpenAI, project_description: str) -> str:
    try:
        user_input = (
            f"Provide a detailed step-by-step workflow for the following project: '{project_description}'. "
            "Include expected outcomes for each step."
        )
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that outlines project workflows with detailed steps and expected outcomes.",
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

