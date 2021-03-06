from cctool.common.lib import default_visualization
from cctool.common.enums import (
    ConnectionOption,
    HeatmapColours,
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
    heatmap_colours = HeatmapColours.__values__

    value = analysis.get(node.identifier, 0)
    node_options['title'] += f'<p>Value: <strong>{str(value*100)}%</strong></p>'
    node_options['value'] = value

    colour_index = round(value * (len(heatmap_colours)-1))
    matched_colour = heatmap_colours[colour_index]
    if matched_colour:
        node_options['color']['border'] = matched_colour
        node_options['color']['background'] = matched_colour
    
    node_options['font']['background'] = MapColours.NODE_FONT_BACKGROUND.value

    return node_options

def generate_edge_options(edge, analysis):
    edge_options = default_visualization.generate_edge_options(edge)

    edge_options['width'] = 1
    edge_options['color'] = MapColours.EDGE_COLOR_DEFAULT.value
    edge_options['highlight'] = MapColours.EDGE_HIGHLIGHT_DEFAULT.value

    return edge_options

def generate_legend():
    legend = default_visualization.generate_legend()
    heatmap_colours = HeatmapColours.__values__

    size = 16
    step_x = size*2
    step_y = 85
    x = 185 - (size*2*(len(heatmap_colours)/2)) + size
    y = legend['structure']['nodes'][-1].get('y',0) + step_y
    id = int(legend['structure']['nodes'][-1].get('id',0)) + 1

    # Find the intersection of nodes and edges (key: label for first edge)
    edge_index = len(legend['structure']['nodes']) - 1
    for i, node in enumerate(legend['structure']['nodes']):
        if node.get('label') == ConnectionOption.COMPLEX_CONNECTION.value:
            node['label'] = 'Default'
            edge_index = i
            y = node['y'] + step_y
    legend['structure']['nodes'] = legend['structure']['nodes'][0:edge_index+2]
    legend['structure']['edges'] = legend['structure']['edges'][0:1]

    for i, colour in enumerate(heatmap_colours):
        label = ''
        if i%4 == 0:
            label = f"{i*5}%"
        node = NodePlus(identifier=str(id), label=label, position_x=x, position_y=y)
        data = node.to_json(use_dict=True)
        vis = generate_node_options(node, {})
        vis.pop('value')
        vis['color']['border'] = colour
        vis['color']['background'] = colour
        vis['shape'] = 'square'
        vis['shapeProperties']['static'] = True
        vis['size'] = size
        legend['structure']['nodes'].append(dict(**data, **vis))
        id = id+1
        x = x+step_x

    return legend