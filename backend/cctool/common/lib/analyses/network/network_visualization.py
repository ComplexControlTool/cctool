from cctool.common.lib import default_visualization
from cctool.common.enums import (
    ConnectionOption,
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

    value = analysis.get(int(node.identifier), 0)
    node_options['title'] += f'<p>Value: <strong>{str(value*100)}%</strong></p>'
    node_options['value'] = value

    top_n = 5
    if node.identifier in analysis.get('ranked',[])[:top_n]:
        node_options['color']['background'] = MapColours.NODE_BACKGROUND_FOCUSED.value

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

    # Find the intersection of nodes and edges (key: label for first edge)
    edge_index = len(legend['structure']['nodes']) - 1
    for i, node in enumerate(legend['structure']['nodes']):
        # get new y value
        if node.get('label') == ConnectionOption.COMPLEX_CONNECTION.value:
            edge_index = i
            y = node['y']
        if i >= edge_index:
            node['y'] += step_y

    more_nodes = [
        NodePlus(identifier=id, label='Focused', position_x=x, position_y=y)
    ]

    for node in more_nodes:
        data = node.to_json(use_dict=True)
        vis = generate_node_options(node, {})
        if 'Focused' in node.label:
            vis['color']['background'] = MapColours.NODE_BACKGROUND_FOCUSED.value
        legend['structure']['nodes'].append(dict(**data, **vis))

    return legend