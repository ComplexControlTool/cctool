from cctool.common.lib import default_visualization


def generate_graph_options():
    graph_options = default_visualization.generate_graph_options()

    graph_options['edges']['smooth']['type'] = 'cubicBezier'
    graph_options['edges']['smooth']['forceDirection'] = 'vertical'
    graph_options['edges']['smooth']['roundness'] = 0.4

    hierarchical = dict()
    hierarchical['enabled'] = True
    hierarchical['direction'] = 'UD'
    hierarchical['nodeSpacing'] = 200
    graph_options['layout']['hierarchical'] = hierarchical

    return graph_options

def generate_node_options(node, analysis):
    node_options = default_visualization.generate_node_options(node)
    node_options['level'] = 0
    root_nodes = [analysis.get('root_node', None)]
    downstream_nodes_and_levels = analysis.get('downstream_nodes_and_levels', {})

    selected_node_mark = '#03A9F4'
    outcome_node = '#FF9800' 
    intervention_node = '#CDDC39'

    if node.tags:
        if 'Outcome' in node.tags:
            node_options['color']['border'] = outcome_node
            node_options['color']['background'] = outcome_node
        if 'Intervention' in node.tags:
            node_options['color']['border'] = intervention_node
            node_options['color']['background'] = intervention_node 
    if node.identifier in downstream_nodes_and_levels:
        node_options['level'] = downstream_nodes_and_levels[node.identifier]
    if node.identifier in root_nodes:
        node_options['color']['border'] = selected_node_mark
        node_options['color']['background'] = outcome_node

    return node_options 
    

def generate_edge_options(edge, analysis):
    return default_visualization.generate_edge_options(edge)