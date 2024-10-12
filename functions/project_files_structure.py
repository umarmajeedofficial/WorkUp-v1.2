# functions/project_files_structure.py

import os
import shutil
import tempfile
import zipfile
import openai
from typing import Dict, Any

def generate_project_files_structure(client: Any, project_description: str, team_members: list, preferences: Dict[str, Any]) -> bytes:
    """
    Generates a dynamic project folder structure based on the project description, team expertise, and user preferences.
    
    Args:
        client (Any): The OpenAI client instance.
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

        response = client.Completion.create(
            engine=preferences.get('model_name', 'text-davinci-003'),
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

def parse_structure(structure_text: str) -> Dict:
    """
    Parses a tree-like structure text into a nested dictionary.

    Args:
        structure_text (str): The tree-like structure text.

    Returns:
        Dict: Nested dictionary representing the folder structure.
    """
    structure = {}
    stack = []
    previous_indent = -1

    for line in structure_text.splitlines():
        if not line.strip():
            continue  # Skip empty lines
        indent = len(line) - len(line.lstrip())
        name = line.strip().replace("* ", "").replace("- ", "").replace("+ ", "")

        node = {}
        if '.' in name and not name.endswith('/'):
            # It's a file
            node = None

        if indent > previous_indent:
            if stack:
                parent = stack[-1]
                if isinstance(parent, dict):
                    parent[last_dir][name] = node
            stack.append(node if node is not None else name)
        else:
            while indent <= previous_indent and stack:
                stack.pop()
                previous_indent -= 4  # Assuming 4 spaces per indent
            if stack:
                parent = stack[-1]
                if isinstance(parent, dict):
                    parent[last_dir][name] = node
            stack.append(node if node is not None else name)
        
        if node is not None:
            last_dir = name
            structure[last_dir] = node
        previous_indent = indent

    return structure

def create_folders(base_path: str, structure: Dict):
    """
    Creates folders and files based on the nested dictionary structure.

    Args:
        base_path (str): The base directory where the structure will be created.
        structure (Dict): Nested dictionary representing the folder structure.
    """
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if content is None:
            # It's a file
            with open(path, 'w') as f:
                f.write("# TODO: Add implementation\n")
        else:
            # It's a directory
            os.makedirs(path, exist_ok=True)
            create_folders(path, content)

def add_starter_files(base_path: str, preferences: Dict[str, Any]):
    """
    Adds starter files like README.md, requirements.txt, etc., based on preferences.

    Args:
        base_path (str): The base directory where the files will be added.
        preferences (Dict[str, Any]): User preferences such as preferred programming language.
    """
    # Add README.md
    readme_path = os.path.join(base_path, "README.md")
    with open(readme_path, 'w') as f:
        f.write("# Project Title\n\n")
        f.write("## Description\n\n")
        f.write("## Installation\n\n")
        f.write("## Usage\n\n")
        f.write("## Contributing\n\n")
        f.write("## License\n")

    # Add .gitignore
    gitignore_path = os.path.join(base_path, ".gitignore")
    with open(gitignore_path, 'w') as f:
        f.write("__pycache__/\n*.py[cod]\n.env\n")

    # Add requirements.txt based on preferred language
    if preferences.get('preferred_language', 'Python').lower() == 'python':
        requirements_path = os.path.join(base_path, "requirements.txt")
        with open(requirements_path, 'w') as f:
            f.write("# Add your project dependencies here\n")
    elif preferences.get('preferred_language', 'Python').lower() == 'javascript':
        package_json_path = os.path.join(base_path, "package.json")
        with open(package_json_path, 'w') as f:
            f.write("{\n  \"name\": \"project-name\",\n  \"version\": \"1.0.0\",\n  \"main\": \"index.js\",\n  \"license\": \"MIT\"\n}\n")
    # Add more languages as needed

    # Add a starter main file based on preferred language
    lang = preferences.get('preferred_language', 'Python').lower()
    if lang == 'python':
        main_path = os.path.join(base_path, "main.py")
        with open(main_path, 'w') as f:
            f.write("def main():\n    print('Hello, World!')\n\n\nif __name__ == '__main__':\n    main()\n")
    elif lang == 'javascript':
        index_js_path = os.path.join(base_path, "index.js")
        with open(index_js_path, 'w') as f:
            f.write("function main() {\n    console.log('Hello, World!');\n}\n\nmain();\n")
    # Add more languages as needed
