import graphviz
import tempfile
import streamlit as st

def generate_flowchart(assignment_response: str, workflow_response: str) -> str:
    try:
        # Parse the assignment_response to extract tasks and members
        tasks = {}
        for line in assignment_response.strip().split('\n'):
            if ':' in line:
                member, task = line.split(':', 1)
                tasks[member.strip()] = task.strip()
        
        if not tasks:
            st.error("No tasks found to generate a flowchart.")
            return ""
        
        # You can use workflow_response to add additional context or nodes if needed
        # For now, we will keep it simple and focus on assignment_response
        dot = graphviz.Digraph(comment='Project Flowchart', format='png')
        
        dot.node('Start', 'Project Start')
        dot.node('End', 'Project End')
        
        prev = 'Start'
        for member, task in tasks.items():
            # Sanitize member name to create a valid node name
            node_name = ''.join(e for e in member if e.isalnum() or e == '_')
            if not node_name:
                node_name = f"Member_{list(tasks.keys()).index(member)+1}"
            dot.node(node_name, f"{member}\n{task}")  # Improved node representation
            dot.edge(prev, node_name)
            prev = node_name
        dot.edge(prev, 'End')
        
        # Render the flowchart to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
            dot.render(filename=tmpfile.name, cleanup=True)
            flowchart_path = tmpfile.name + '.png'
        
        return flowchart_path

    except Exception as e:
        st.error(f"Flowchart generation failed: {str(e)}")
        return ""
