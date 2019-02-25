from cctool.common.lib import default_visualization


def generate_graph_options():
    graph_options = default_visualization.generate_graph_options()

    graph_options['edges']['smooth']['type'] = 'cubicBezier'
    graph_options['edges']['smooth']['forceDirection'] = 'vertical'
    graph_options['edges']['smooth']['roundness'] = 0.4

    hierarchical = dict()
    hierarchical['enabled'] = True
    hierarchical['direction'] = 'UD'
    graph_options['layout']['hierarchical'] = hierarchical

    return graph_options

def generate_node_options(node, analysis):
    node_options = default_visualization.generate_node_options(node)
    node_options['level'] = 0
    root_nodes = analysis.data.get('root_nodes', {})
    downstream_nodes_and_levels = analysis.data.get('downstream_nodes_and_levels', {})

    if node.identifier in downstream_nodes_and_levels:
        node_options['level'] = downstream_nodes_and_levels[node.identifier]
    if node.identifier in root_nodes:
        node_options['color']['background'] = '#009900'

    return node_options 
    

def generate_edge_options(edge, analysis):
    return default_visualization.generate_edge_options(edge)