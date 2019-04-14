from cctool.common.lib import default_visualization
from cctool.common.enums import (
    MapColours,
)

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