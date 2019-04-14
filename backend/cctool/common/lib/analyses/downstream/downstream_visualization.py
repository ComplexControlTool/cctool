from cctool.common.lib import default_visualization
from cctool.common.enums import (
    MapColours,
)


def generate_graph_options():
    graph_options = default_visualization.generate_graph_options()
    graph_options['layout'].pop('randomSeed')

    graph_options['edges']['smooth']['type'] = 'cubicBezier'
    graph_options['edges']['smooth']['forceDirection'] = 'vertical'
    graph_options['edges']['smooth']['roundness'] = 0.4

    hierarchical = dict()
    hierarchical['enabled'] = True
    hierarchical['nodeSpacing'] = 150
    hierarchical['direction'] = 'UD'
    hierarchical['sortMethod'] = 'directed'
    graph_options['layout']['hierarchical'] = hierarchical

    physics = dict()
    physics['enabled'] = True
    graph_options['physics'] = physics

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