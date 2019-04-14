from cctool.common.lib import default_visualization


def generate_graph_options():
    graph_options = default_visualization.generate_graph_options()

    label = dict()
    label['enabled'] = True

    scaling = dict()
    scaling['label'] = label

    nodes = dict()
    nodes['scaling'] = scaling

    graph_options['nodes'] = nodes

    return graph_options

def generate_node_options(node, analysis):
    node_options = default_visualization.generate_node_options(node)

    # Override for Frequency
    frequencies = analysis.data.get('frequencies', {})
    if node.identifier in frequencies:
        freq_value = frequencies[node.identifier]
        node_options['value'] = freq_value
        node_options['title'] += f'<p>Frequency: <strong>{str(freq_value)}%</strong></p>'
    else:
        node_options['value'] = 0

    return node_options

def generate_edge_options(edge, analysis):
    edge_options = default_visualization.generate_edge_options(edge)

    return edge_options

