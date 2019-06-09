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
    graph_options['layout'].pop('randomSeed')

    graph_options['edges']['smooth']['type'] = 'cubicBezier'
    graph_options['edges']['smooth']['forceDirection'] = 'vertical'
    graph_options['edges']['smooth']['roundness'] = 0.4

    hierarchical = dict()
    hierarchical['enabled'] = True
    hierarchical['nodeSpacing'] = 300
    hierarchical['direction'] = 'UD'
    hierarchical['sortMethod'] = 'directed'
    graph_options['layout']['hierarchical'] = hierarchical

    return graph_options

def generate_node_options(node, analysis):
    node_options = default_visualization.generate_node_options(node)
    node_options['level'] = 0
    root_nodes = [analysis.get('root_node', None)]
    downstream_nodes_and_levels = analysis.get('downstream_nodes_and_levels', {})

    if node.tags:
        if 'Outcome' in node.tags:
            node_options['color']['background'] = MapColours.NODE_BACKGROUND_OUTCOME.value
        if 'Intervention' in node.tags:
            node_options['color']['background'] = MapColours.NODE_BACKGROUND_INTERVENTION.value 
    if node.identifier in downstream_nodes_and_levels:
        node_options['level'] = downstream_nodes_and_levels[node.identifier]
    if node.identifier in root_nodes:
        node_options['color']['background'] = MapColours.NODE_BACKGROUND_INTERVENTION.value

    return node_options     

def generate_edge_options(edge, analysis):
    return default_visualization.generate_edge_options(edge)

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
        NodePlus(identifier=id, label='Outcome', position_x=x + (0*step_x), position_y=y, tags=['Outcome']),
        NodePlus(identifier=id+1, label='Intervention', position_x=x + (1*step_x), position_y=y, tags=['Intervention'])
    ]

    for node in more_nodes:
        data = node.to_json(use_dict=True)
        vis = generate_node_options(node, {})
        legend['structure']['nodes'].append(dict(**data, **vis))

    return legend