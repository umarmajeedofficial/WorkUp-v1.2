import os
import streamlit as st
from functions import (
    client,
    get_workload_distribution,
    get_project_workflow,
    generate_flowchart,
    generate_project_structure,
    suggest_project_names,
    extract_text,
    display_project_table
)
import tempfile

def main():
    st.set_page_config(page_title="WorkUp - Project Management Automation", layout="wide")
    st.title("WorkUp - Project Management Automation")

    # Sidebar for project configuration and file uploads
    st.sidebar.header("Project Configuration")

    # File input for project description
    project_file = st.sidebar.file_uploader("Upload Project Description", type=["pdf", "docx", "txt"])
    if project_file:
        project_description = extract_text(project_file)
        if project_description:
            st.sidebar.success("Project description loaded from file.")
    else:
        project_description = st.sidebar.text_area("Enter Project Description", height=200)

    # File input for teammates' expertise
    expertise_file = st.sidebar.file_uploader("Upload Team Members' Expertise", type=["pdf", "docx", "txt"])
    if expertise_file:
        expertise_text = extract_text(expertise_file)
        if expertise_text:
            team_members = [line.strip() for line in expertise_text.splitlines() if line.strip()]
            st.sidebar.success("Team members' expertise loaded from file.")
    else:
        num_team_members = st.sidebar.number_input("Number of Team Members", min_value=1, max_value=20, step=1, value=2)
        team_members = []
        for i in range(num_team_members):
            st.sidebar.subheader(f"Member {i + 1}")
            name = st.sidebar.text_input(f"Name of Member {i + 1}", key=f"name_{i + 1}")
            expertise = st.sidebar.text_area(f"Expertise of Member {i + 1}", key=f"expertise_{i + 1}", height=100)
            if name and expertise:
                team_members.append({"name": name.strip(), "expertise": expertise.strip()})

    # Store outputs in session state
    if 'outputs' not in st.session_state:
        st.session_state.outputs = {}

    # Main area
    st.header("Project Overview")

    if project_description:
        st.subheader("Project Description")
        st.write(project_description)
    else:
        st.warning("Please provide a project description.")

    if team_members:
        st.subheader("Team Members")
        for member in team_members:
            st.write(f"**{member['name']}**: {member['expertise']}")
    else:
        st.warning("Please provide team members' information.")

    # Button to trigger the task assignment and other functions
    if st.button("Start Project Setup"):
        # Validate inputs
        missing_info = []
        if not project_description.strip():
            missing_info.append("Project description")
        if not team_members:
            missing_info.append("Team members' names and expertise")

        if missing_info:
            st.error(f"Please provide the following missing information: {', '.join(missing_info)}.")
        else:
            try:
                # Workload Distribution
                with st.spinner("Assigning tasks based on team expertise..."):
                    assignment_response = get_workload_distribution(client, project_description, team_members)
                    st.session_state.outputs['assignment_response'] = assignment_response

                # Project Workflow
                with st.spinner("Generating project workflow..."):
                    workflow_response = get_project_workflow(client, project_description)
                    st.session_state.outputs['workflow_response'] = workflow_response

                # Flowchart Generation
                with st.spinner("Generating flowchart..."):
                    flowchart_path = generate_flowchart(workflow_response)
                    st.session_state.outputs['flowchart_path'] = flowchart_path

                # Project Structure and Code Generation
                with st.spinner("Generating project structure and starter code..."):
                    project_zip = generate_project_structure(assignment_response)
                    st.session_state.outputs['project_zip'] = project_zip

                # Project Naming Suggestions
                with st.spinner("Generating project name suggestions..."):
                    naming_response = suggest_project_names(client, project_description)
                    st.session_state.outputs['naming_response'] = naming_response

                # Display outputs
                display_outputs(st.session_state.outputs)

            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")

    # Download buttons for various outputs
    if 'assignment_response' in st.session_state.outputs:
        st.subheader("Task Assignments and Project Summary")
        st.write(st.session_state.outputs['assignment_response'])
        # Download Task Assignments
        if st.button("Download Task Assignments"):
            with open("task_assignments.txt", "w") as f:
                f.write(st.session_state.outputs['assignment_response'])
            st.download_button("Download", "task_assignments.txt", "text/plain")

    if 'workflow_response' in st.session_state.outputs:
        st.subheader("Project Workflow")
        st.write(st.session_state.outputs['workflow_response'])
        # Download Workflow
        if st.button("Download Project Workflow"):
            with open("project_workflow.txt", "w") as f:
                f.write(st.session_state.outputs['workflow_response'])
            st.download_button("Download", "project_workflow.txt", "text/plain")

    if 'flowchart_path' in st.session_state.outputs:
        st.subheader("Project Flowchart")
        st.image(st.session_state.outputs['flowchart_path'], use_column_width=True)
        if st.button("Download Flowchart"):
            with open(st.session_state.outputs['flowchart_path'], "rb") as img_file:
                st.download_button("Download Flowchart", img_file, "image/png")

    if 'project_zip' in st.session_state.outputs:
        st.subheader("Download Project Structure")
        st.download_button("Download Project Folder", st.session_state.outputs['project_zip'], "application/zip")

    if 'naming_response' in st.session_state.outputs:
        st.subheader("Project Name Suggestions")
        st.write(st.session_state.outputs['naming_response'])

def display_outputs(outputs):
    if 'assignment_response' in outputs:
        st.success("Tasks Assigned Successfully!")
        st.write(outputs['assignment_response'])

    if 'workflow_response' in outputs:
        st.success("Project Workflow Generated!")
        st.write(outputs['workflow_response'])

    if 'flowchart_path' in outputs:
        st.success("Flowchart Generated!")
        st.image(outputs['flowchart_path'], use_column_width=True)

    if 'project_zip' in outputs:
        st.success("Project Structure Generated!")

    if 'naming_response' in outputs:
        st.success("Project Names Suggested!")
        st.write(outputs['naming_response'])

if __name__ == "__main__":
    main()
