import matplotlib.pyplot as plt
import networkx as nx
import tempfile
import streamlit as st
import random

def generate_flowchart(workload_distribution: str) -> str:
    try:
        # Parse the workload_distribution to extract tasks and assignments
        tasks = {}
        for line in workload_distribution.split('\n'):
            if ':' in line:
                member, task = line.split(':', 1)
                tasks[member.strip()] = task.strip()
        
        if not tasks:
            st.error("No tasks found to generate a flowchart.")
            return ""
        
        # Create a directed graph
        G = nx.DiGraph()
        G.add_node('Start', label='Start')
        G.add_node('End', label='End')

        prev = 'Start'
        colors = ["#d3d3d3"]  # Color for the Start node
        unique_members = list(set(tasks.keys()))
        member_colors = {member: f"#{random.randint(0, 0xFFFFFF):06x}" for member in unique_members}  # Assign random color for each member

        for member, task in tasks.items():
            node_name = ''.join(e for e in member if e.isalnum() or e == '_')
            if not node_name:
                node_name = f"Member_{list(tasks.keys()).index(member) + 1}"
            G.add_node(node_name, label=f"{member}\n{task}")
            G.add_edge(prev, node_name)
            prev = node_name
            colors.append(member_colors[member])  # Add color based on member

        G.add_edge(prev, 'End')
        colors.append("#d3d3d3")  # Color for 'End' node

        # Choose a better layout for flowcharts
        pos = nx.shell_layout(G)  # Better layout for a flowchart

        # Draw the flowchart with distinct colors and labels
        plt.figure(figsize=(10, 8))
        nx.draw(
            G, pos, 
            with_labels=True, 
            labels=nx.get_node_attributes(G, 'label'),
            node_size=3000, 
            node_color=colors,  # Apply different colors to members
            font_size=10, 
            font_color='black', 
            font_weight='bold', 
            arrows=True,
            edge_color="gray"
        )

        # Save the flowchart to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
            plt.savefig(tmpfile.name, format='png')
            plt.close()  # Close the plot to free memory
            flowchart_path = tmpfile.name
        
        return flowchart_path

    except Exception as e:
        st.error(f"Flowchart generation failed: {str(e)}")
        return ""
