
import networkx as nx
import matplotlib.pyplot as plt

def draw_neural_network(input_neurons, hidden_layers, output_neurons, directed_edges=True):
    # Create a directed or undirected graph
    G = nx.DiGraph() if directed_edges else nx.Graph()
    
    # Calculate positions for each layer with even spacing
    pos = {}
    total_layers = len(hidden_layers) + 2  # Input + hidden + output
    layer_x = [i * 1.0 for i in range(total_layers)]  # Ensure equal spacing
    
    all_nodes = []  # Keep track of all nodes for coloring
    node_color_map = []
    node_labels = {}  # Dictionary to store node labels
    activation_labels = []  # List for activation function labels
   
    def extract_color(layer_tuple):
        if len(layer_tuple) > 2 and isinstance(layer_tuple[2], str):
            return layer_tuple[2]  # Assume third element is color if it's a string
        return "grey"  # Default color

    # Function to handle large layers by collapsing middle nodes
    def get_visible_nodes(neurons):
        if neurons <= 6:
            return list(range(neurons))  # Show all if <= 6
        return list(range(3)) + ["..."] + list(range(neurons - 3, neurons))  # Show first 3, last 3, collapse middle

    # Function to determine vertical positions (ensuring top to bottom numbering)
    def get_y_positions(neurons):
        return [(neurons - 1) / 2 - i for i in range(neurons)]

    # Input layer
    input_count, input_color, input_label = input_neurons if len(input_neurons) == 3 else (input_neurons[0], input_neurons[1], True)
    input_color = str(input_color)  # Ensure it's a string
    input_y = get_visible_nodes(input_count)
    input_positions = get_y_positions(len(input_y))
    
    for i, (y, y_pos) in enumerate(zip(input_y, input_positions)):
        node_name = f'input_{y}' if y != "..." else "input_ellipsis"
        pos[node_name] = (0, y_pos)
        G.add_node(node_name)
        all_nodes.append(node_name)
        node_color_map.append("white" if y == "..." else input_color)  # Transparent color for ellipsis node
        if input_label and y != "...":
            node_labels[node_name] = f"x{y+1}"  # Label as x1, x2, x3...

    # Hidden layers
    current_x = 1
    min_y_position = float('inf')  # Track lowest y-position for alignment
    for layer_idx, layer in enumerate(hidden_layers):
        neurons, activation = layer[0], layer[1]
        layer_color = extract_color(layer)  # Get valid color
        label_flag = layer[-1] if isinstance(layer[-1], bool) else True  # Check last item for boolean flag
        
        layer_y = get_visible_nodes(neurons)
        layer_positions = get_y_positions(len(layer_y))
        
        for i, (y, y_pos) in enumerate(zip(layer_y, layer_positions)):
            node_name = f'hidden_{layer_idx}_{y}' if y != "..." else f'hidden_{layer_idx}_ellipsis'
            pos[node_name] = (current_x, y_pos)
            G.add_node(node_name)
            all_nodes.append(node_name)
            node_color_map.append("white" if y == "..." else layer_color)  # Ensure middle nodes remain white  # Transparent color for ellipsis node
            if label_flag and y != "...":
                node_labels[node_name] = f"h{layer_idx+1}{y+1}"  # Label as h11, h12, h13, etc.

        # Store activation function label position (far left under the edges)
        min_y_position = min(min_y_position, min(layer_positions))
        activation_labels.append((current_x - 0.5, activation))

        current_x += 1
    
    # Output layer
    output_neurons_count, output_activation, output_color, output_label = output_neurons if len(output_neurons) == 4 else (
        output_neurons[0], output_neurons[1], extract_color(output_neurons), True)
    output_color = str(output_color)  # Ensure it's a string
    
    output_y = get_visible_nodes(output_neurons_count)
    output_positions = get_y_positions(len(output_y))
    
    for i, (y, y_pos) in enumerate(zip(output_y, output_positions)):
        node_name = f'output_{y}' if y != "..." else "output_ellipsis"
        pos[node_name] = (current_x, y_pos)
        G.add_node(node_name)
        all_nodes.append(node_name)
        node_color_map.append("white" if y == "..." else output_color)  # Transparent color for ellipsis node
        if output_label and y != "...":
            node_labels[node_name] = f"y{y+1}"  # Label as y1, y2, y3...

    # Store activation function label for output (far left under the edges)
    activation_labels.append((current_x - 0.5, output_activation))

    # Add edges (excluding "..." placeholders)
    for layer_idx in range(len(hidden_layers) + 1):
        if layer_idx == 0:
            from_nodes = [f'input_{i}' for i in get_visible_nodes(input_count) if isinstance(i, int)]
            to_nodes = [f'hidden_0_{i}' for i in get_visible_nodes(hidden_layers[0][0]) if isinstance(i, int)]
        elif layer_idx == len(hidden_layers):
            from_nodes = [f'hidden_{layer_idx-1}_{i}' for i in get_visible_nodes(hidden_layers[layer_idx-1][0]) if isinstance(i, int)]
            to_nodes = [f'output_{i}' for i in get_visible_nodes(output_neurons_count) if isinstance(i, int)]
        else:
            from_nodes = [f'hidden_{layer_idx-1}_{i}' for i in get_visible_nodes(hidden_layers[layer_idx-1][0]) if isinstance(i, int)]
            to_nodes = [f'hidden_{layer_idx}_{i}' for i in get_visible_nodes(hidden_layers[layer_idx][0]) if isinstance(i, int)]

        for fn in from_nodes:
            for tn in to_nodes:
                if fn in pos and tn in pos:
                    G.add_edge(fn, tn)

    # Draw the graph
    plt.figure(figsize=(8, 3))  # Increase figure height for better spacing
    nx.draw(G, pos, with_labels=False, node_color=node_color_map, node_size=300, edge_color='black', width=0.3, arrows=directed_edges)

    # Draw labels selectively
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)

    # Draw ellipsis (three black dots) for collapsed nodes
    for node in pos:
        if "ellipsis" in node:
            x, y = pos[node]
            plt.text(x, y, "⋮", fontsize=12, fontweight='bold', color='black', horizontalalignment='center', verticalalignment='center')

    # Top labels for each layer
    label_y_fixed_top = max([v[1] for v in pos.values()]) * 1.3  # Scale dynamically

    layer_labels = ["Input"] + [f"Hidden{idx+1}" for idx in range(len(hidden_layers))] + ["Output"]
    for idx, label in enumerate(layer_labels):
        layer_x_pos = layer_x[idx]
        plt.text(layer_x_pos, label_y_fixed_top, label, horizontalalignment='center', fontsize=10, color='black', fontweight='bold')

    # Bottom labels (activation functions)
    activation_y_position = min([v[1] for v in pos.values()]) * 1.3  # Scale dynamically
    for x_pos, activation_text in activation_labels:
        plt.text(x_pos, activation_y_position, activation_text, horizontalalignment='left', fontsize=8, color='black', fontstyle='italic')

    plt.axis('off')
    plt.tight_layout()
    plt.show()
