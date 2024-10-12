import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def generate_flowchart(workload_distribution: str) -> None:
    try:
        # Parse the workload_distribution to extract tasks and assignments
        tasks = {}
        for line in workload_distribution.split('\n'):
            if ':' in line:
                member, task = line.split(':', 1)
                tasks[member.strip()] = task.strip()
        
        if not tasks:
            st.error("No tasks found to generate a flowchart.")
            return
        
        # Create a flowchart using Matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        
        # Create flowchart nodes and edges
        node_positions = {}
        node_height = 1  # Height of each node

        # Start node
        ax.text(5, 9, "Project Start", ha='center', va='center', bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round,pad=0.5'))
        node_positions['Start'] = (5, 9)

        prev_y = 8  # Start position for the first task
        for member, task in tasks.items():
            # Set node position
            node_positions[member] = (5, prev_y)
            ax.text(5, prev_y, f"{member}\n{task}", ha='center', va='center', bbox=dict(facecolor='lightgreen', edgecolor='black', boxstyle='round,pad=0.5'))
            prev_y -= node_height

            # Draw edge from the previous node to the current node
            if member != 'Start':
                ax.plot([5, 5], [prev_y + node_height, prev_y], color='black')

        # End node
        ax.text(5, prev_y, "Project End", ha='center', va='center', bbox=dict(facecolor='lightcoral', edgecolor='black', boxstyle='round,pad=0.5'))

        # Turn off the axes
        ax.axis('off')
        plt.tight_layout()

        # Show the plot in Streamlit
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Flowchart generation failed: {str(e)}")
