import matplotlib.pyplot as plt
import networkx as nx

def generate_flowchart_matplotlib(assignment_response: str, workflow_response: str) -> None:
    # Parse the assignment_response to extract tasks and members
    tasks = {}
    for line in assignment_response.strip().split('\n'):
        if ':' in line:
            member, task = line.split(':', 1)
            tasks[member.strip()] = task.strip()
    
    if not tasks:
        st.error("No tasks found to generate a flowchart.")
        return

    # Create a directed graph
    G = nx.DiGraph()
    G.add_node('Start')
    G.add_node('End')

    prev = 'Start'
    for member, task in tasks.items():
        node_name = ''.join(e for e in member if e.isalnum() or e == '_')
        G.add_node(node_name, label=f"{member}\n{task}")
        G.add_edge(prev, node_name)
        prev = node_name
    G.add_edge(prev, 'End')

    # Draw the graph
    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw(G, pos, with_labels=True, arrows=True)
    labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(G, pos, labels)

    # Show the plot
    plt.title("Project Flowchart")
    plt.show()
