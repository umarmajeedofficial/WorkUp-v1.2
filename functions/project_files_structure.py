# functions/project_files_structure.py

import os
import tempfile
import zipfile
import openai
from typing import Dict, Any
from config import MODEL_NAME  # Import the model name from config instead of DEFAULT_MODEL_NAME

def generate_project_files_structure(project_description: str, team_members: list, preferences: Dict[str, Any]) -> bytes:
    """
    Generates a dynamic project folder structure based on the project description, team expertise, and user preferences.
    
    Args:
        project_description (str): Description of the project.
        team_members (list): List of team members with their expertise.
        preferences (Dict[str, Any]): User preferences such as preferred programming language.
    
    Returns:
        bytes: Bytes of the zipped project structure.
    """
    try:
        # Step 1: Use OpenAI to generate a suggested project structure
        prompt = (
            f"Based on the following project description and team expertise, suggest a comprehensive folder and file structure "
            f"for a GitHub repository. The structure should include directories, subdirectories, and essential files. "
            f"Consider the preferred programming language: {preferences.get('preferred_language', 'Python')}.\n\n"
            f"Project Description:\n{project_description}\n\n"
            f"Team Members and Expertise:\n"
        )
        for member in team_members:
            prompt += f"- {member['name']}: {member['expertise']}\n"

        prompt += "\nProvide the folder structure in a tree format."

        response = openai.Completion.create(
            engine=preferences.get('model_name', MODEL_NAME),  # Use MODEL_NAME instead of DEFAULT_MODEL_NAME
            prompt=prompt,
            max_tokens=500,
            temperature=0.5,
            n=1,
            stop=None
        )

        structure_text = response.choices[0].text.strip()

        # Step 2: Parse the structure text into a nested dictionary
        structure = parse_structure(structure_text)

        # Step 3: Create the folder structure in a temporary directory
        with tempfile.TemporaryDirectory() as tmpdirname:
            create_folders(tmpdirname, structure)

            # Optionally, add some starter files based on preferences
            add_starter_files(tmpdirname, preferences)

            # Step 4: Zip the directory
            zip_buffer = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
            with zipfile.ZipFile(zip_buffer.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(tmpdirname):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, tmpdirname)
                        zipf.write(file_path, arcname)
            
            # Read the zip file bytes
            with open(zip_buffer.name, 'rb') as f:
                zip_bytes = f.read()
            
            # Clean up the temporary zip file
            os.unlink(zip_buffer.name)
        
        return zip_bytes

    except Exception as e:
        raise RuntimeError(f"Failed to generate project structure: {str(e)}")

# The rest of the functions remain unchanged...
