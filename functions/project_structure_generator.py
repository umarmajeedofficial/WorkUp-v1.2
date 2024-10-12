import os
import zipfile

def generate_dynamic_project_structure(workflow_output):
    # Define a basic project structure template based on workflow output
    project_structure = {
        "app.py": "# Main application entry point\n\nif __name__ == '__main__':\n    pass",
        "requirements.txt": "flask\nnumpy\npandas\n# Add more dependencies based on project needs",
        "README.md": "# Project Title\n\n## Description\n\n# Installation Instructions\n\n# Usage\n\n# License",
    }
    
    # Dynamically add folders and files based on the workflow_output
    for task in workflow_output:
        # Assuming each task has a name and type (like "backend", "frontend", etc.)
        task_name = task.get("name", "default_task").replace(" ", "_").lower()
        task_type = task.get("type", "general")  # Example task type, modify as needed

        # Create a folder for each task
        project_structure[f"{task_name}/"] = None  # Use None to indicate it's a folder

        # Depending on task type, add specific files
        if task_type == "backend":
            project_structure[f"{task_name}/models.py"] = "# Models for the backend"
            project_structure[f"{task_name}/controllers.py"] = "# Controllers for handling requests"
        elif task_type == "frontend":
            project_structure[f"{task_name}/components.py"] = "# React components for frontend"
            project_structure[f"{task_name}/styles.css"] = "/* CSS Styles */"
        elif task_type == "data":
            project_structure[f"{task_name}/data_processing.py"] = "# Data processing scripts"
    
    # Create a temporary directory to store the project structure
    temp_dir = "temp_project_structure"
    os.makedirs(temp_dir, exist_ok=True)

    # Create files and directories
    for path, content in project_structure.items():
        full_path = os.path.join(temp_dir, path)
        if content is None:  # It's a directory
            os.makedirs(full_path, exist_ok=True)
        else:  # It's a file
            with open(full_path, 'w') as f:
                f.write(content)

    # Create a zip file of the project structure
    zip_filename = "project_structure.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_dir))

    # Cleanup the temporary directory
    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(temp_dir)

    return zip_filename
