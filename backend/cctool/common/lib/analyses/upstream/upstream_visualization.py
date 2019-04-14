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
    hierarchical['direction'] = 'DU'
    hierarchical['nodeSpacing'] = 200
    graph_options['layout']['hierarchical'] = hierarchical

    return graph_options

def generate_node_options(node, analysis):
    node_options = default_visualization.generate_node_options(node)
    node_options['level'] = 0
    root_nodes = [analysis.get('root_node', None)]
    upstream_nodes_and_levels = analysis.get('upstream_nodes_and_levels', {})

    if node.tags:
        if 'Outcome' in node.tags:
            node_options['color']['background'] = MapColours.NODE_BACKGROUND_OUTCOME.value
        if 'Intervention' in node.tags:
            node_options['color']['background'] = MapColours.NODE_BACKGROUND_INTERVENTION.value 
    if node.identifier in upstream_nodes_and_levels:
        node_options['level'] = upstream_nodes_and_levels[node.identifier]
    if node.identifier in root_nodes:
        node_options['color']['background'] = MapColours.NODE_BACKGROUND_OUTCOME.value

    return node_options 

def generate_edge_options(edge, analysis):
    return default_visualization.generate_edge_options(edge)