from cctool.common.lib import default_visualization
from cctool.common.enums import (
    MapColours,
)
from cctool.graphs.models import (
    NodePlus
)


def generate_graph_options():
    graph_options = default_visualization.generate_graph_options()

    label = dict()
    label['enabled'] = True
    label['min'] = 12
    label['max'] = 18

    scaling = dict()
    scaling['min'] = 10
    scaling['max'] = 20
    scaling['label'] = label

    nodes = dict()
    nodes['scaling'] = scaling

    graph_options['nodes'] = nodes

    return graph_options

def generate_node_options(node, analysis):
    node_options = default_visualization.generate_node_options(node)

    # Override for Frequency
    if analysis:
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

def generate_legend():
    legend = default_visualization.generate_legend()

    step_x = 185
    step_y = 85
    x = 0
    y = legend['structure']['nodes'][-1].get('y',0) + step_y
    id = legend['structure']['nodes'][-1].get('id',0) + 1

    more_nodes = [
        NodePlus(identifier=id, label='Focused', position_x=x, position_y=y)
    ]

    for i, node in enumerate(more_nodes):
        visualization = generate_node_options(node, {})
        if 'Focused' in node.label:
            visualization['color']['background'] = MapColours.NODE_BACKGROUND_FOCUSED.value
        legend['structure']['nodes'].append(dict(**node.to_json(use_dict=True), **visualization))

    return legend