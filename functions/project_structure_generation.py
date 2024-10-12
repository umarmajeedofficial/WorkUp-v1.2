# functions/project_structure_generation.py

import os
import zipfile
import tempfile
from typing import List
import streamlit as st

def generate_project_structure(workload_distribution: str) -> bytes:
    try:
        # Parse tasks
        tasks = {}
        for line in workload_distribution.split('\n'):
            if ':' in line:
                member, task = line.split(':', 1)
                tasks[member.strip()] = task.strip()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create project folders
            os.makedirs(os.path.join(temp_dir, 'src'), exist_ok=True)
            os.makedirs(os.path.join(temp_dir, 'tests'), exist_ok=True)
            os.makedirs(os.path.join(temp_dir, 'docs'), exist_ok=True)
            
            # Create starter code files
            for member, task in tasks.items():
                filename = f"{member.replace(' ', '_').lower()}.py"
                filepath = os.path.join(temp_dir, 'src', filename)
                with open(filepath, 'w') as f:
                    f.write(f"# Starter code for {member}\n\ndef {task.replace(' ', '_')}():\n    pass\n")
            
            # Create requirements.txt
            with open(os.path.join(temp_dir, 'requirements.txt'), 'w') as f:
                f.write("streamlit\nopenai\n")
            
            # Zip the project folder
            zip_path = os.path.join(temp_dir, 'project_structure.zip')
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file != 'project_structure.zip':
                            zipf.write(os.path.join(root, file), arcname=os.path.relpath(os.path.join(root, file), temp_dir))
            
            # Read the zip file
            with open(zip_path, 'rb') as f:
                zip_bytes = f.read()
            
            return zip_bytes

    except Exception as e:
        st.error(f"Project structure generation failed: {str(e)}")
        return b""

