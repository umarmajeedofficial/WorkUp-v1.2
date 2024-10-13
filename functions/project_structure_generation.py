import os
import zipfile
import tempfile
import re  # Import regex for sanitizing filenames
from typing import List
import streamlit as st

def sanitize_filename(name: str) -> str:
    """
    Removes or replaces invalid characters from a filename.
    
    Args:
        name (str): The original filename.
    
    Returns:
        str: The sanitized filename.
    """
    # Remove any characters that are not alphanumeric, underscores, or hyphens
    return re.sub(r'[^\w\-]', '_', name)

def generate_project_structure(workload_distribution: str, project_description: str, project_deliverables: str) -> bytes:
    try:
        # Parse tasks
        tasks = {}
        for line in workload_distribution.split('\n'):
            if ':' in line:
                member, task = line.split(':', 1)
                tasks[sanitize_filename(member.strip())] = task.strip()

        if not tasks:
            st.error("No tasks found to generate project structure.")
            return b""

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create project docs
            docs_path = os.path.join(temp_dir, 'project_docs')
            os.makedirs(docs_path, exist_ok=True)
            
            # Write project description
            with open(os.path.join(docs_path, 'project_description.txt'), 'w') as f:
                f.write(project_description)

            # Write project deliverables
            with open(os.path.join(docs_path, 'project_deliverables.txt'), 'w') as f:
                f.write(project_deliverables)

            # Create member task files
            for member, task in tasks.items():
                filepath = os.path.join(docs_path, f"{member}_task.txt")
                with open(filepath, 'w') as f:
                    f.write(f"Task for {member}: {task}\n")

            # Create project code directory
            code_dir = os.path.join(temp_dir, 'project_code')
            os.makedirs(code_dir, exist_ok=True)

            # Create starter code files based on tasks (assumes tasks are backend or frontend)
            for member in tasks.keys():
                if 'backend' in tasks[member].lower():
                    code_content = f"# Starter backend code for {member}\n\ndef start_backend():\n    pass\n"
                else:
                    code_content = f"# Starter frontend code for {member}\n\ndef start_frontend():\n    pass\n"

                filename = f"{member}_code.py"
                filepath = os.path.join(code_dir, filename)
                with open(filepath, 'w') as f:
                    f.write(code_content)

            # Create requirements.txt
            with open(os.path.join(temp_dir, 'requirements.txt'), 'w') as f:
                f.write("streamlit\nopenai\n")  # Add any additional dependencies here

            # Zip the project folder
            zip_path = os.path.join(temp_dir, 'project_structure.zip')
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file != 'project_structure.zip':
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, temp_dir)
                            zipf.write(file_path, arcname=arcname)

            # Read the zip file
            with open(zip_path, 'rb') as f:
                zip_bytes = f.read()

            return zip_bytes

    except Exception as e:
        st.error(f"Project structure generation failed: {str(e)}")
        return b""
