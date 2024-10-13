# app.py

import os
import streamlit as st
import time
from functions import (
    client,
    get_workload_distribution,
    get_project_workflow,
    generate_flowchart,
    generate_project_structure,
    suggest_project_names,
    extract_text
)

import tempfile

def display_welcome_messages():
    """Display a typing animation for the welcome messages."""
    if 'welcome_messages_displayed' not in st.session_state:
        st.session_state.welcome_messages_displayed = True
        
        welcome_messages = [
            "Welcome to WorkUp!",
            "How may I assist you?",
            "What can I do for you?",
            "Let's make project management easier!",
            "Ready to automate your project setup?",
            "Your project management assistant is here!",
            "Let's get started on your project!",
            "Transforming project ideas into reality!",
            "Empowering your team with automation!",
            "Let's streamline your workflow!"
        ]
        
        text_placeholder = st.empty()  # Placeholder for the text
        for message in welcome_messages:
            # Typing effect
            for i in range(len(message) + 1):
                text_placeholder.markdown(f"<h3 style='color: black; font-size: 16px;'>{message[:i]}</h3>", unsafe_allow_html=True)
                time.sleep(0.1)  # Typing speed
            time.sleep(1)  # Wait before clearing the message
            # Clear message
            text_placeholder.markdown("<h3 style='color: black; font-size: 16px;'> </h3>", unsafe_allow_html=True)
            time.sleep(0.5)  # Pause before next message

        # After displaying all messages, clear the placeholder
        text_placeholder.empty()








# Import for session management and feedback
from streamlit.runtime.scriptrunner.script_runner import StopException

# For handling feedback storage
if 'feedback' not in st.session_state:
    st.session_state['feedback'] = []

def main():
    # Set page configuration
    st.set_page_config(page_title="WorkUp - Project Management Automation", layout="wide")
    st.title("WorkUp - Project Management Automation")

    # Call the welcome message display function in a separate thread
    if 'welcome_displayed' not in st.session_state:
        st.session_state.welcome_displayed = True
        display_welcome_messages()

    # Initialize session state for feedback
    if 'feedback' not in st.session_state:
        st.session_state.feedback = []

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
            # Assuming each team member's expertise is separated by a delimiter, e.g., '---'
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
        # Manual input for team members
        num_team_members = st.sidebar.number_input(
            "Number of Team Members",
            min_value=1,
            max_value=20,
            step=1,
            value=2,
            help="Select the number of team members."
        )

        team_members = []
        for i in range(1, num_team_members + 1):
            st.sidebar.subheader(f"Member {i}")
            name = st.sidebar.text_input(f"Name of Member {i}", key=f"name_{i}")
            expertise = st.sidebar.text_area(f"Expertise of Member {i}", key=f"expertise_{i}", height=100)
            if name and expertise:
                team_members.append({"name": name.strip(), "expertise": expertise.strip()})
    
    # User Interface Enhancements: Additional Preferences
    st.sidebar.subheader("Preferences")
    preferred_language = st.sidebar.selectbox(
        "Preferred Programming Language",
        options=["Python", "JavaScript", "Java", "C++", "Other"],
        index=0
    )
    other_options = st.sidebar.text_input("Other Project-Specific Options")
    
    # Centralized Configuration Management is already handled via config.py

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
            # Initialize placeholders for incremental display
            assignment_placeholder = st.empty()
            workflow_placeholder = st.empty()
            flowchart_placeholder = st.empty()
            structure_placeholder = st.empty()
            naming_placeholder = st.empty()
            
            try:
                # Workload Distribution
                with st.spinner("Assigning tasks based on team expertise..."):
                    assignment_response = get_workload_distribution(client, project_description, team_members)
                    assignment_placeholder.success("Tasks Assigned Successfully!")
                    assignment_placeholder.subheader("Task Assignments and Project Summary")
                    assignment_placeholder.write(assignment_response)
                
                # Project Workflow
                with st.spinner("Generating project workflow..."):
                    workflow_response = get_project_workflow(client, project_description)
                    workflow_placeholder.success("Project Workflow Generated!")
                    workflow_placeholder.subheader("Project Workflow")
                    workflow_placeholder.write(workflow_response)
                
                # Flowchart Generation
                with st.spinner("Generating flowchart..."):
                    flowchart_path = generate_flowchart(assignment_response, workflow_response)
                    if flowchart_path:
                        flowchart_placeholder.success("Flowchart Generated!")
                        flowchart_placeholder.subheader("Project Flowchart")
                        flowchart_placeholder.image(flowchart_path, use_column_width=True)
                        with open(flowchart_path, "rb") as img_file:
                            btn = st.download_button(
                                label="Download Flowchart",
                                data=img_file,
                                file_name="flowchart.png",
                                mime="image/png"
                            )
                
                # Project Structure and Code Generation
                with st.spinner("Generating project structure and starter code..."):
                    project_zip = generate_project_structure(assignment_response)
                    if project_zip:
                        structure_placeholder.success("Project Structure Generated!")
                        structure_placeholder.subheader("Download Project Structure")
                        structure_placeholder.download_button(
                            label="Download Project Folder",
                            data=project_zip,
                            file_name="project_structure.zip",
                            mime="application/zip"
                        )
                
                # Project Naming Suggestions
                with st.spinner("Generating project name suggestions..."):
                    naming_response = suggest_project_names(client, project_description)
                    naming_placeholder.success("Project Names Suggested!")
                    naming_placeholder.subheader("Project Name Suggestions")
                    naming_placeholder.write(naming_response)
                
                # Project Naming Feedback
                feedback = st.text_area("Provide Feedback on the Project Setup:", height=100)
                if st.button("Submit Feedback", key="submit_feedback_main"):
                    if feedback.strip():
                        st.session_state.feedback.append(feedback.strip())
                        st.success("Thank you for your feedback!")
                    else:
                        st.error("Feedback cannot be empty.")

            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
    
    # Continuous Interaction Loop with Session Management and Feedback
    st.sidebar.markdown("---")
    if st.sidebar.button("Reset Session", key="reset_session"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()

    st.sidebar.subheader("Feedback")
    st.sidebar.write("Your feedback helps us improve the application.")
    user_feedback = st.sidebar.text_input("Enter your feedback:")
    if st.sidebar.button("Submit Feedback", key="submit_feedback_sidebar"):
        if user_feedback.strip():
            st.session_state.feedback.append(user_feedback.strip())
            st.sidebar.success("Thank you for your feedback!")
        else:
            st.sidebar.error("Feedback cannot be empty.")

    # Display Feedback (for demonstration purposes; in production, you might store it securely)
    if st.checkbox("Show Submitted Feedback"):
        if st.session_state.feedback:
            st.write("### Submitted Feedback:")
            for idx, fb in enumerate(st.session_state.feedback, 1):
                st.write(f"{idx}. {fb}")
        else:
            st.write("No feedback submitted yet.")

if __name__ == "__main__":
    main()
