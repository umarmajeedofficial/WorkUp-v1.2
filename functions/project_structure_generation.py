# functions/project_structure_generation.py

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

def generate_project_structure(workload_distribution: str) -> bytes:
    try:
        # Parse tasks
        tasks = {}
        for line in workload_distribution.split('\n'):
            if ':' in line:
                member, task = line.split(':', 1)
                tasks[member.strip()] = task.strip()
        
        if not tasks:
            st.error("No tasks found to generate project structure.")
            return b""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create project folders
            os.makedirs(os.path.join(temp_dir, 'src'), exist_ok=True)
            os.makedirs(os.path.join(temp_dir, 'tests'), exist_ok=True)
            os.makedirs(os.path.join(temp_dir, 'docs'), exist_ok=True)
            
            # Create starter code files
            for idx, (member, task) in enumerate(tasks.items(), start=1):
                sanitized_member = sanitize_filename(member)
                filename = f"{idx}_{sanitized_member}.py"
                filepath = os.path.join(temp_dir, 'src', filename)
                with open(filepath, 'w') as f:
                    f.write(f"# Starter code for {member}\n\ndef {sanitize_filename(task)}():\n    pass\n")
            
            # Create requirements.txt
            with open(os.path.join(temp_dir, 'requirements.txt'), 'w') as f:
                f.write("streamlit\nopenai\n")
            
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
