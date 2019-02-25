from cctool.common.lib import default_visualization
from cctool.graphs.models.models import NodePlus, EdgePlus


def generate_graph_options():
    return default_visualization.generate_graph_options()

def generate_node_options(node, analysis):
    node_options = default_visualization.generate_node_options(node)

    # Override for Controllability
    try:
        if node.controllability == NodePlus.EASY_CONTROLLABILITY:
            node_options['color']['highlight']['background'] = '#74c476'
            node_options['color']['border'] = '#238b45'
            node_options['color']['background'] = '#74c476'
        elif node.controllability == NodePlus.MEDIUM_CONTROLLABILITY:
            node_options['color']['highlight']['background'] = '#fdae6b'
            node_options['color']['border'] = '#fd8d3c'
            node_options['color']['background'] = '#fdae6b'
        elif node.controllability == NodePlus.HARD_CONTROLLABILITY:
            node_options['color']['highlight']['background'] = '#fb6a4a'
            node_options['color']['border'] = '#cb181d'
            node_options['color']['background'] = '#fb6a4a'
    except AttributeError:
        pass

    # Override for Importance
    try:
        if node.importance == NodePlus.LOW_IMPORTANCE:
            node_options['shapeProperties']['borderDashes'] = [2,4]
        elif node.importance == NodePlus.HIGH_IMPORTANCE:
            node_options['borderWidth'] = 3
            node_options['shapeProperties']['borderDashes'] = [15,10]
    except AttributeError:
        pass

    # Override for Frequency
    frequencies = analysis.data.get('frequencies', {})
    if node.identifier in frequencies:
        freq_value = frequencies[node.identifier]
        defaultRadius = 13
        added_radius = freq_value / 100 * 15
        node_options['size'] = defaultRadius + added_radius
        node_options['title'] += f'<p>Frequency: <strong>{str(freq_value)}%</strong></p>'

    return node_options

def generate_edge_options(edge, analysis):
    edge_options = default_visualization.generate_edge_options(edge)

    try:
        if edge.weight == EdgePlus.POSITIVE_WEAK_WEIGHT:
            edge_options['color']['color'] = '#c7e9c0'
            edge_options['color']['highlight'] = '#c7e9c0'
        elif edge.weight == EdgePlus.POSITIVE_MEDIUM_WEIGHT:
            edge_options['color']['color'] = '#41ab5d'
            edge_options['color']['highlight'] = '#41ab5d'
        elif edge.weight == EdgePlus.POSITIVE_STRONG_WEIGHT:
            edge_options['color']['color'] = '#00441b'
            edge_options['color']['highlight'] = '#00441b'
        elif edge.weight == EdgePlus.NEGATIVE_WEAK_WEIGHT:
            edge_options['color']['color'] = '#fcbba1'
            edge_options['color']['highlight'] = '#fcbba1'
        elif edge.weight == EdgePlus.NEGATIVE_MEDIUM_WEIGHT:
            edge_options['color']['color'] = '#fb6a4a'
            edge_options['color']['highlight'] = '#fb6a4a'
        elif edge.weight == EdgePlus.NEGATIVE_STRONG_WEIGHT:
            edge_options['color']['color'] = '#cb181d'
            edge_options['color']['highlight'] = '#cb181d'
    except AttributeError:
        pass

    return edge_options

