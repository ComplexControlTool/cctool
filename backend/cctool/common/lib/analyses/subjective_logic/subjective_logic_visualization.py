from cctool.common.lib import default_visualization


def generate_graph_options():
    graph_options = default_visualization.generate_graph_options()
    graph_options['layout']['randomSeed'] = 2

    return graph_options

def generate_node_options(node, analysis):
    node_options = default_visualization.generate_node_options(node)
    colour_spectrum = [
        '#1d4877', '#255672', '#29636c', '#287166', '#237f5f', 
        '#358c58', '#6f9650', '#9a9e46', '#c2a63b', '#e8ad2c',
        '#fbac24', '#faa42a', '#f99b2f', '#f89333', '#f68a37',
        '#f57e37', '#f47036', '#f26135', '#f05133', '#ee3e32'
    ] # http://gka.github.io/palettes/#colors=#1d4877,#1b8a5a,#fbb021,#f68838,#ee3e32|steps=20|bez=0|coL=0

    value = analysis.get(int(node.identifier), 0)
    if value > 1.0:
        value = 1.0
    color_index = round(value * (len(colour_spectrum)-1))
    matched_color = colour_spectrum[color_index]
    if matched_color:
        node_options['color']['border'] = matched_color
        node_options['color']['background'] = matched_color

    return node_options
    

def generate_edge_options(edge, analysis):
    edge_options = default_visualization.generate_edge_options(edge)

    return edge_options