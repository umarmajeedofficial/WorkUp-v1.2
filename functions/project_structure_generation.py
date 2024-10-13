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

        # Create a temporary directory to hold project files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Project documentation file
            documentation_path = os.path.join(temp_dir, 'project_documentation.txt')
            with open(documentation_path, 'w') as doc_file:
                doc_file.write("Project Documentation\n")
                doc_file.write("===================================\n")
                doc_file.write("Overview:\n")
                doc_file.write("This project aims to build a state-of-the-art application that utilizes advanced AI technologies.\n\n")
                doc_file.write("Objectives and Goals:\n")
                doc_file.write("1. Develop a user-friendly interface.\n")
                doc_file.write("2. Implement backend services for data processing.\n")
                doc_file.write("3. Ensure high performance and scalability.\n\n")
                doc_file.write("Team Member Tasks:\n")

                # Initialize tasks and members
                tasks = {}
                for line in lines:
                    if ':' in line:
                        member, task = line.split(':', 1)
                        sanitized_member = sanitize_filename(member.strip())
                        task_detail = task.strip()
                        tasks[sanitized_member] = task_detail
                        doc_file.write(f"- {sanitized_member}: {task_detail}\n")

            if not tasks:
                st.error("No tasks found to generate project structure.")
                return b""

            # Create project code structure folder
            code_structure_path = os.path.join(temp_dir, 'project_code_structure')
            os.makedirs(code_structure_path, exist_ok=True)

            # Create Python files based on member tasks and initial code structure
            for idx, (member, task) in enumerate(tasks.items(), start=1):
                # Create a Python file for each member's task
                task_filename = f"{member}_task.py"
                task_filepath = os.path.join(code_structure_path, task_filename)
                with open(task_filepath, 'w') as f:
                    f.write(f"# Task assigned to {member}\n")
                    f.write(f"def {sanitize_filename(task)}():\n")
                    f.write("    # Placeholder for implementation\n")
                    f.write("    print(f'Executing task: {task}')\n")
                    f.write("    # More code goes here\n")
                    f.write("    # Simulating task completion...\n")
                    f.write("    return 'Task Completed'\n\n")
                    f.write(f"# Example usage:\n")
                    f.write(f"if __name__ == '__main__':\n")
                    f.write(f"    result = {sanitize_filename(task)}()\n")
                    f.write(f"    print(result)\n")

            # Create initial code files (e.g., app.py and other relevant files)
            initial_files = {
                'app.py': """from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the AI Project!"

if __name__ == "__main__":
    app.run(debug=True)
""",
                'database.py': """import sqlite3

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def initialize_database():
    conn = create_connection('project.db')
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                        (id INTEGER PRIMARY KEY,
                        task TEXT NOT NULL);''')
    conn.close()
""",
                'utils.py': """def log_task(task):
    print(f'Task logged: {task}')

def send_notification(message):
    print(f'Notification: {message}')
"""
            }

            # Write the initial code files
            for filename, content in initial_files.items():
                filepath = os.path.join(code_structure_path, filename)
                with open(filepath, 'w') as f:
                    f.write(content)

            # Create requirements.txt
            with open(os.path.join(code_structure_path, 'requirements.txt'), 'w') as f:
                f.write("streamlit\nopenai\nflask\n")  # Add more dependencies as needed

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
