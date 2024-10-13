# # functions/flowchart_generation.py

# import graphviz
# import tempfile  # Add this import
# from typing import Dict
# import streamlit as st

# def generate_flowchart(workload_distribution: str, project_workflow: str) -> str:
#     try:
#         # Parse the workload_distribution and project_workflow to extract tasks and assignments
#         # For simplicity, assume that workload_distribution contains lines like "Member: Task"
#         tasks = {}
#         for line in workload_distribution.split('\n'):
#             if ':' in line:
#                 member, task = line.split(':', 1)
#                 tasks[member.strip()] = task.strip()
        
#         if not tasks:
#             st.error("No tasks found to generate a flowchart.")
#             return ""
        
#         # Create a flowchart
#         dot = graphviz.Digraph(comment='Project Flowchart', format='png')
        
#         dot.node('Start', 'Project Start')
#         dot.node('End', 'Project End')
        
#         prev = 'Start'
#         for member, task in tasks.items():
#             # Sanitize member name to create a valid node name
#             node_name = ''.join(e for e in member if e.isalnum() or e == '_')
#             if not node_name:
#                 node_name = f"Member_{list(tasks.keys()).index(member)+1}"
#             dot.node(node_name, f"{member}\n{task}")
#             dot.edge(prev, node_name)
#             prev = node_name
#         dot.edge(prev, 'End')
        
#         # Render the flowchart to a temporary file
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
#             dot.render(filename=tmpfile.name, cleanup=True)
#             flowchart_path = tmpfile.name + '.png'
        
#         return flowchart_path

#     except Exception as e:
#         st.error(f"Flowchart generation failed: {str(e)}")
#         return ""



import matplotlib.pyplot as plt
import networkx as nx
import tempfile
import streamlit as st

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
        G.add_node('Start')
        G.add_node('End')
        
        prev = 'Start'
        for member, task in tasks.items():
            node_name = ''.join(e for e in member if e.isalnum() or e == '_')
            if not node_name:
                node_name = f"Member_{list(tasks.keys()).index(member)+1}"
            G.add_node(node_name, label=f"{member}\n{task}")
            G.add_edge(prev, node_name)
            prev = node_name
        G.add_edge(prev, 'End')

        # Draw the flowchart
        pos = nx.spring_layout(G)  # You can change the layout as needed
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'), node_size=3000, node_color='lightblue', font_size=10, font_color='black', font_weight='bold', arrows=True)

        # Save the flowchart to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
            plt.savefig(tmpfile.name, format='png')
            plt.close()  # Close the plot to free memory
            flowchart_path = tmpfile.name
        
        return flowchart_path

    except Exception as e:
        st.error(f"Flowchart generation failed: {str(e)}")
        return ""
