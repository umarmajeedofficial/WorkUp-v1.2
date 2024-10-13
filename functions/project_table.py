# functions/project_table.py

import pandas as pd
import streamlit as st
from typing import List, Dict
from .utils import sanitize_filename  # Import the sanitize function


def generate_project_table(team_members: List[Dict[str, str]]) -> pd.DataFrame:
    """
    Generates a pandas DataFrame representing the project table.

    Args:
        team_members (List[Dict[str, str]]): A list of dictionaries containing team member names and their tasks.

    Returns:
        pd.DataFrame: A DataFrame with the project table.
    """
    # Create a DataFrame from team members
    data = {
        "Team Member": [member['name'] for member in team_members],
        "Assigned Task": [member.get('task', 'N/A') for member in team_members]
    }
    df = pd.DataFrame(data)

    return df


def display_project_table(team_members: List[Dict[str, str]]):
    """
    Displays the project table in Streamlit.

    Args:
        team_members (List[Dict[str, str]]): A list of dictionaries containing team member names and their tasks.
    """
    if not team_members:
        st.warning("No team members to display.")
        return

    df = generate_project_table(team_members)
    st.markdown("### Team Members and Assigned Tasks")
    st.table(df)

    # Option to download the table as CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Project Table as CSV",
        data=csv,
        file_name="project_table.csv",
        mime="text/csv",
    )
