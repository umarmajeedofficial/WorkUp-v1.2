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
        # Split the workload distribution into lines
        lines = workload_distribution.split('\n')
        
        # Create project documentation
        with open('project_description.txt', 'w') as f:
            f.write("Project Overview:\n")
            f.write("This project aims to build a state-of-the-art application that utilizes advanced AI technologies.\n\n")
            f.write("Objectives and Goals:\n")
            f.write("1. Develop a user-friendly interface.\n")
            f.write("2. Implement backend services for data processing.\n")
            f.write("3. Ensure high performance and scalability.\n")

        # Initialize tasks and members
        tasks = {}
        for line in lines:
            if ':' in line:
                member, task = line.split(':', 1)
                tasks[member.strip()] = task.strip()
        
        if not tasks:
            st.error("No tasks found to generate project structure.")
            return b""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create project folders
            os.makedirs(os.path.join(temp_dir, 'project_code_structure'), exist_ok=True)
            
            # Create project deliverables file
            with open(os.path.join(temp_dir, 'project_deliverables.txt'), 'w') as f:
                f.write("Project Deliverables:\n")
                f.write("1. A fully functional web application.\n")
                f.write("2. Comprehensive user documentation.\n")
                f.write("3. Source code with detailed comments.\n")
            
            # Create member work distribution files
            for idx, (member, task) in enumerate(tasks.items(), start=1):
                sanitized_member = sanitize_filename(member)
                filename = f"{sanitized_member}_work.txt"
                filepath = os.path.join(temp_dir, f"{filename}")
                with open(filepath, 'w') as f:
                    f.write(f"Work assigned to {member}:\n")
                    f.write(f"{task}\n")
            
            # Create initial code files based on project type
            if "backend" in workload_distribution.lower():
                with open(os.path.join(temp_dir, 'project_code_structure', 'app.py'), 'w') as f:
                    f.write("# Main application code\n")
                    f.write("if __name__ == '__main__':\n")
                    f.write("    pass\n")
                with open(os.path.join(temp_dir, 'project_code_structure', 'database.py'), 'w') as f:
                    f.write("# Database connection and models\n")
                    f.write("def connect_db():\n")
                    f.write("    pass\n")
            else:
                with open(os.path.join(temp_dir, 'project_code_structure', 'index.html'), 'w') as f:
                    f.write("<!DOCTYPE html>\n<html>\n<head>\n    <title>Project</title>\n</head>\n<body>\n</body>\n</html>\n")
                with open(os.path.join(temp_dir, 'project_code_structure', 'styles.css'), 'w') as f:
                    f.write("/* Styles for the project */\n")
                with open(os.path.join(temp_dir, 'project_code_structure', 'script.js'), 'w') as f:
                    f.write("// JavaScript code for the project\n")

            # Create requirements.txt
            with open(os.path.join(temp_dir, 'project_code_structure', 'requirements.txt'), 'w') as f:
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
