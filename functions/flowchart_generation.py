import matplotlib.pyplot as plt
import networkx as nx
import tempfile
import streamlit as st
from openai import OpenAI, OpenAIError
from config import MODEL_NAME

# Util function to interact with the Llama model (based on your existing pattern)
def ask_llama_for_graph_suggestion(client: OpenAI, assignment_response: str) -> str:
    try:
        user_input = (
            f"I have the following response describing project tasks and team expertise:\n'{assignment_response}'.\n"
            "Please analyze the input and tell me what type of graph I should create to best represent this information, "
            "along with any suggestions for how to structure it."
        )

        # Send the request to Llama (OpenAI API) to get the best graph suggestion
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI that provides suggestions for graph creation based on input descriptions.",
                },
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
        )

        # Extract and return the Llama model's response
        message = response.choices[0].message.content
        return message

    except OpenAIError as e:
        return f"API request failed: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


def generate_flowchart(client: OpenAI, workload_distribution: str, assignment_response: str) -> str:
    try:
        # Step 1: Ask Llama model for graph suggestions based on assignment_response
        llama_suggestion = ask_llama_for_graph_suggestion(client, assignment_response)
        st.write(f"Llama model suggests: {llama_suggestion}")

        # Step 2: Parse the workload_distribution to extract tasks and assignments
        tasks = {}
        for line in workload_distribution.split('\n'):
            if ':' in line:
                member, task = line.split(':', 1)
                tasks[member.strip()] = task.strip()

        if not tasks:
            st.error("No tasks found to generate a graph.")
            return ""

        # Step 3: Create a graph based on the suggestion from the Llama model
        G = nx.DiGraph()  # Using a directed graph for flowchart or dependency graphs
        
        if "flowchart" in llama_suggestion.lower():
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
        
        elif "dependency" in llama_suggestion.lower():
            # Add logic to create a dependency graph structure
            for member, task in tasks.items():
                G.add_node(member, label=f"{member}\n{task}")
                # Example of adding dependencies (can be customized)
                if "depends on" in task.lower():
                    dependencies = task.split("depends on", 1)[1].strip().split(',')
                    for dep in dependencies:
                        dep_node = dep.strip()
                        if dep_node in tasks:
                            G.add_edge(dep_node, member)
        
        else:
            # Basic graph with only nodes
            for member, task in tasks.items():
                G.add_node(member, label=f"{member}\n{task}")
        
        # Step 4: Draw the graph
        pos = nx.spring_layout(G)  # You can change the layout as needed
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'), 
                node_size=3000, node_color='lightblue', font_size=10, font_color='black', 
                font_weight='bold', arrows=True)

        # Step 5: Save the graph to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
            plt.savefig(tmpfile.name, format='png')
            plt.close()  # Close the plot to free memory
            graph_path = tmpfile.name
        
        return graph_path

    except Exception as e:
        st.error(f"Graph generation failed: {str(e)}")
        return ""
