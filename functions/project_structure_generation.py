import os
import zipfile
import tempfile
import re  # Import regex for sanitizing filenames
from typing import Dict
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
        tasks: Dict[str, str] = {}
        for line in workload_distribution.split('\n'):
            if ':' in line:
                member, task = line.split(':', 1)
                tasks[member.strip()] = task.strip()
        
        if not tasks:
            st.error("No tasks found to generate project structure.")
            return b""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create project directories
            os.makedirs(os.path.join(temp_dir, 'project_docs'), exist_ok=True)
            os.makedirs(os.path.join(temp_dir, 'project_code'), exist_ok=True)

            # Create project description file
            with open(os.path.join(temp_dir, 'project_docs', 'project_description.txt'), 'w') as f:
                f.write(project_description)
            
            # Create deliverables file
            with open(os.path.join(temp_dir, 'project_docs', 'project_deliverables.txt'), 'w') as f:
                f.write(project_deliverables)

            # Create task files for each member
            for member, task in tasks.items():
                sanitized_member = sanitize_filename(member)
                filepath = os.path.join(temp_dir, 'project_docs', f"{sanitized_member}_tasks.txt")
                with open(filepath, 'w') as f:
                    f.write(f"{member}'s Task: {task}\n")

            # Create starter code files in the project_code directory
            for idx, member in enumerate(tasks.keys(), start=1):
                sanitized_member = sanitize_filename(member)
                code_filename = f"{idx}_{sanitized_member}.py"
                filepath = os.path.join(temp_dir, 'project_code', code_filename)

                # Simple starter code based on type (frontend/backend)
                if 'backend' in tasks[sanitized_member].lower():
                    code_content = (
                        f"# Starter code for {member}\n"
                        f"def {sanitized_member}_api():\n"
                        "    # TODO: Implement the API\n"
                        "    pass\n"
                    )
                else:
                    code_content = (
                        f"# Starter code for {member}\n"
                        f"def {sanitized_member}_component():\n"
                        "    # TODO: Implement the frontend component\n"
                        "    pass\n"
                    )

                with open(filepath, 'w') as f:
                    f.write(code_content)

            # Create requirements.txt
            with open(os.path.join(temp_dir, 'requirements.txt'), 'w') as f:
                f.write("streamlit\nopenai\n")  # Add other dependencies as needed
            
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
