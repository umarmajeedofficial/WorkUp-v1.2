# functions/workload_distribution.py

from typing import List, Dict
from openai import OpenAI, OpenAIError
from config import MODEL_NAME
from .utils import extract_text

def get_workload_distribution(client: OpenAI, project_description: str, team_members: List[Dict[str, str]]) -> str:
    try:
        # Construct expertise list
        expertise_list = "\n".join([f"{member['name']}: {member['expertise']}" for member in team_members])
        
        user_input = (
            f"The project is described as: '{project_description}'.\n"
            f"The following team members with different expertise are involved:\n{expertise_list}.\n"
            "Please intelligently assign tasks based on their expertise, "
            "summarize the project, and provide expected outcomes."
        )
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant who assigns project tasks intelligently based on expertise, summarizes project details, and provides expected outcomes.",
                },
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
        )

        # Extract and return the assistant's response
        message = response.choices[0].message.content
        return message

    except OpenAIError as e:
        return f"API request failed: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

