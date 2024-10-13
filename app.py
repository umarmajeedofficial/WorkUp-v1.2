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

# Initialize session state variables
if 'assignment_response' not in st.session_state:
    st.session_state['assignment_response'] = None
if 'workflow_response' not in st.session_state:
    st.session_state['workflow_response'] = None
if 'flowchart_path' not in st.session_state:
    st.session_state['flowchart_path'] = None
if 'project_zip' not in st.session_state:
    st.session_state['project_zip'] = None
if 'naming_response' not in st.session_state:
    st.session_state['naming_response'] = None

def main():
    # Set page configuration
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
            team_members = []
            members = expertise_text.split('---')
            for member in members:
                lines = member.strip().split('\n')
                if len(lines) >= 2:
                    name = lines[0].strip()
                    expertise = ' '.join(lines[1:]).strip()
                    team_members.append({"name": name, "expertise": expertise})
            st.sidebar.success("Team members' expertise loaded from file.")
    else:
        num_team_members = st.sidebar.number_input("Number of Team Members", min_value=1, max_value=20, step=1, value=2)
        team_members = []
        for i in range(1, num_team_members + 1):
            st.sidebar.subheader(f"Member {i}")
            name = st.sidebar.text_input(f"Name of Member {i}", key=f"name_{i}")
            expertise = st.sidebar.text_area(f"Expertise of Member {i}", key=f"expertise_{i}", height=100)
            if name and expertise:
                team_members.append({"name": name.strip(), "expertise": expertise.strip()})

    st.sidebar.subheader("Preferences")
    preferred_language = st.sidebar.selectbox("Preferred Programming Language", options=["Python", "JavaScript", "Java", "C++", "Other"], index=0)
    other_options = st.sidebar.text_input("Other Project-Specific Options")

    st.sidebar.markdown("---")
    st.sidebar.info("Provide project description and team members' expertise either via upload or manual input.")

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
    if st.button("Start Project Setup", key="start_project_setup"):
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
                    st.session_state['assignment_response'] = get_workload_distribution(client, project_description, team_members)
                    st.success("Tasks Assigned Successfully!")

                # Project Workflow
                with st.spinner("Generating project workflow..."):
                    st.session_state['workflow_response'] = get_project_workflow(client, project_description)
                    st.success("Project Workflow Generated!")

                # Flowchart Generation
                with st.spinner("Generating flowchart..."):
                    st.session_state['flowchart_path'] = generate_flowchart(st.session_state['workflow_response'])
                    st.success("Flowchart Generated!")

                # Project Structure and Code Generation
                with st.spinner("Generating project structure and starter code..."):
                    st.session_state['project_zip'] = generate_project_structure(st.session_state['assignment_response'])
                    st.success("Project Structure Generated!")

                # Project Naming Suggestions
                with st.spinner("Generating project name suggestions..."):
                    st.session_state['naming_response'] = suggest_project_names(client, project_description)
                    st.success("Project Names Suggested!")

            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")

    # Display project details if available
    if st.session_state['assignment_response']:
        st.subheader("Task Assignments and Project Summary")
        st.write(st.session_state['assignment_response'])

    if st.session_state['workflow_response']:
        st.subheader("Project Workflow")
        st.write(st.session_state['workflow_response'])

    if st.session_state['flowchart_path']:
        st.subheader("Project Flowchart")
        st.image(st.session_state['flowchart_path'], use_column_width=True)
        with open(st.session_state['flowchart_path'], "rb") as img_file:
            st.download_button(label="Download Flowchart", data=img_file, file_name="flowchart.png", mime="image/png")

    if st.session_state['project_zip']:
        st.subheader("Download Project Structure")
        st.download_button(label="Download Project Folder", data=st.session_state['project_zip'], file_name="project_structure.zip", mime="application/zip")

    if st.session_state['naming_response']:
        st.subheader("Project Name Suggestions")
        st.write(st.session_state['naming_response'])

    # Parse and display project table
    if st.session_state['assignment_response']:
        team_tasks = []
        for line in st.session_state['assignment_response'].split('\n'):
            if ':' in line:
                member, task = line.split(':', 1)
                team_tasks.append({"name": member.strip(), "task": task.strip()})
        display_project_table(team_tasks)

if __name__ == "__main__":
    main()
