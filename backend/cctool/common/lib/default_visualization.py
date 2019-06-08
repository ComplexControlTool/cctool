from cctool.common.enums import (
    ControllabilityOption,
    ControllabilityShortcode,
    VulnerabilityOption,
    VulnerabilityShortcode,
    ImportanceOption,
    ImportanceShortcode,
    ConnectionOption,
    ConnectionShortcode,
    MapColours,
)
from cctool.graphs.models import (
    NodePlus,
    EdgePlus
)


def generate_graph_options():
    graph_options = dict()

    arrows_to = dict()
    arrows_to['enabled'] = True
    arrows_to['scaleFactor'] = 1
    arrows_to['type'] = 'arrow'

    arrows = dict()
    arrows['to'] = arrows_to
    
    color = dict()
    color['hover'] = MapColours.HOVER_DEFAULT.value
    color['opacity'] = 1.0

    smooth = dict()
    smooth['enabled'] = True
    smooth['type'] = 'continuous'
    smooth['roundness'] = 0.5

    edges = dict()
    edges['arrows'] = arrows
    edges['color'] = color
    edges['selectionWidth'] = 2
    edges['smooth'] = smooth

    interaction = dict()
    interaction['hover'] = True
    interaction['navigationButtons'] = True

    layout = dict()
    layout['randomSeed'] = 2

    physics = dict()
    physics['enabled'] = False

    graph_options['autoResize'] = True
    graph_options['width'] = '100%'
    graph_options['height'] = '100%'
    graph_options['locale'] = 'en'
    graph_options['clickToUse'] = True
    graph_options['edges'] = edges
    graph_options['interaction'] = interaction
    graph_options['layout'] = layout
    graph_options['physics'] = physics

    return graph_options

def generate_node_options(node):
    node_options = dict()

    borderWidth = 2

    borderWidthSelected = 2

    highlight = dict()
    highlight['border'] = MapColours.NODE_HIGHLIGHT_BORDER_DEFAULT.value
    highlight['background'] = MapColours.NODE_HIGHLIGHT_BACKGROUND_DEFAULT.value

    hover = dict()
    hover['border'] = MapColours.NODE_HOVER_BORDER_DEFAULT.value
    hover['background'] = MapColours.NODE_HOVER_BACKGROUND_DEFAULT.value

    color = dict()
    color['border'] = MapColours.NODE_BORDER_DEFAULT.value
    color['background'] = MapColours.NODE_BACKGROUND_DEFAULT.value
    color['highlight'] = highlight
    color['hover'] = hover

    font = dict()
    font['size'] = 14

    labelHighlightBold = True

    shape = "ellipse"

    shape_properties = dict()
    shape_properties['borderDashes'] = False

    size = 13

    title = list()
    try:
        title.append(f'<p><strong>{node.label}</strong></p>')
    except AttributeError:
        pass
    try:
        title.append(f'<p>Controllability: <strong>{node.get_controllability_display()}</strong></p>')
    except AttributeError:
        pass
    try:
        title.append(f'<p>Vulnerability: <strong>{node.get_vulnerability_display()}</strong></p>')
    except AttributeError:
        pass
    try:
        title.append(f'<p>Importance: <strong>{node.get_importance_display()}</strong></p>')
    except AttributeError:
        pass
    try:
        title.append(f'<p>Function: <strong>{node.get_function_display()}</strong></p>')
    except AttributeError:
        pass

    try:
        if node.custom:
            for label,value in node.custom.items():
                title.append(f'<p>{label}: <strong>{value}</strong></p>')
    except AttributeError:
        pass
    try:
        if node.tags:
            tags = ' | '.join(node.tags)
            title.append(f'<p>Tags: <strong>{tags}</strong></p>')
    except AttributeError:
        pass

    node_options['borderWidth'] = borderWidth
    node_options['borderWidthSelected'] = borderWidthSelected
    node_options['color'] = color
    node_options['font'] = font
    node_options['labelHighlightBold'] = labelHighlightBold
    node_options['shape'] = shape
    node_options['shapeProperties'] = shape_properties
    node_options['size'] = size
    node_options['title'] = ''.join(title)

    try:
        if not node.position_x in [None, '']:
            node_options['x'] = node.position_x
    except AttributeError:
        pass
    try:
        if not node.position_y in [None, '']:
            node_options['y'] = node.position_y
    except AttributeError:
        pass

    # Define specifics for attributes: Controllability, Vulnerability, Importance
    shadow = dict()
    shadow['enabled'] = True

    # Controllability
    try:
        if node.controllability == ControllabilityShortcode.HIGH_CONTROLLABILITY.value:
            node_options['color']['highlight']['border'] = MapColours.NODE_HIGHLIGHT_BORDER_HIGH_CONTROLLABILITY.value
            node_options['color']['border'] = MapColours.NODE_BORDER_HIGH_CONTROLLABILITY.value
        elif node.controllability == ControllabilityShortcode.MEDIUM_CONTROLLABILITY.value:
            node_options['color']['highlight']['border'] = MapColours.NODE_HIGHLIGHT_BORDER_MEDIUM_CONTROLLABILITY.value
            node_options['color']['border'] = MapColours.NODE_BORDER_MEDIUM_CONTROLLABILITY.value
        elif node.controllability == ControllabilityShortcode.LOW_CONTROLLABILITY.value:
            node_options['color']['highlight']['border'] = MapColours.NODE_HIGHLIGHT_BORDER_LOW_CONTROLLABILITY.value
            node_options['color']['border'] = MapColours.NODE_BORDER_LOW_CONTROLLABILITY.value
    except AttributeError:
        pass

    # Vulnerability
    try:
        # if node.vulnerability == VulnerabilityShortcode.LOW_VULNERABILITY.value:
        #     node_options['shapeProperties']['borderDashes'] = [2,3]
        # elif node.vulnerability == VulnerabilityShortcode.MEDIUM_VULNERABILITY.value:
        #     node_options['shapeProperties']['borderDashes'] = [4,6]
        if node.vulnerability == VulnerabilityShortcode.HIGH_VULNERABILITY.value:
            node_options['shapeProperties']['borderDashes'] = [8,12]
    except AttributeError:
        pass

    # Importance
    try:
        # if node.importance == ImportanceShortcode.LOW_IMPORTANCE.value:
        #     node_options['color']['background'] = MapColours.NODE_BACKGROUND_LOW_IMPORTANCE.value
        if node.importance == ImportanceShortcode.HIGH_IMPORTANCE.value:
            node_options['color']['background'] = MapColours.NODE_BACKGROUND_HIGH_IMPORTANCE.value
    except AttributeError:
        pass

    return node_options

def generate_edge_options(edge):
    edge_options = dict()

    color = dict()
    color['color'] = MapColours.EDGE_COLOR_DEFAULT.value
    color['highlight'] = MapColours.EDGE_HIGHLIGHT_DEFAULT.value

    labelHighlightBold = True

    title = list()
    try:
        title.append(f'<p>From:</p><p><strong>{edge.source.label}</strong></p><p>To:</p><p><strong>{edge.target.label}</strong></p>')
    except AttributeError:
        pass
    try:
        title.append(f'<p>Connection Weight: <strong>{edge.get_weight_display()}</strong></p>')
    except AttributeError:
        pass

    width = 1

    edge_options['color'] = color
    edge_options['labelHighlightBold'] = labelHighlightBold
    edge_options['title'] = ''.join(title)
    edge_options['width'] = width

    # Define specifics for attributes: Weight
    font = dict()
    font['size'] = 16
    font['align'] = 'bottom'

    # Weight
    try:
        sign = ''
        if edge.weight == ConnectionShortcode.POSITIVE_WEAK_CONNECTION.value:
            edge_options['color']['color'] = MapColours.EDGE_COLOR_POSITIVE_WEAK_CONNECTION.value
            edge_options['color']['highlight'] = MapColours.EDGE_HIGHLIGHT_POSITIVE_WEAK_CONNECTION.value
            sign = '+'
        elif edge.weight == ConnectionShortcode.POSITIVE_MEDIUM_CONNECTION.value:
            edge_options['color']['color'] = MapColours.EDGE_COLOR_POSITIVE_MEDIUM_CONNECTION.value
            edge_options['color']['highlight'] = MapColours.EDGE_HIGHLIGHT_POSITIVE_MEDIUM_CONNECTION.value
            edge_options['width'] = 2
            sign = '+'
        elif edge.weight == ConnectionShortcode.POSITIVE_STRONG_CONNECTION.value:
            edge_options['color']['color'] = MapColours.EDGE_COLOR_POSITIVE_STRONG_CONNECTION.value
            edge_options['color']['highlight'] = MapColours.EDGE_HIGHLIGHT_POSITIVE_STRONG_CONNECTION.value
            edge_options['width'] = 4
            sign = '+'
        elif edge.weight == ConnectionShortcode.NEGATIVE_WEAK_CONNECTION.value:
            edge_options['color']['color'] = MapColours.EDGE_COLOR_NEGATIVE_WEAK_CONNECTION.value
            edge_options['color']['highlight'] = MapColours.EDGE_HIGHLIGHT_NEGATIVE_WEAK_CONNECTION.value
            sign = '-'
        elif edge.weight == ConnectionShortcode.NEGATIVE_MEDIUM_CONNECTION.value:
            edge_options['color']['color'] = MapColours.EDGE_COLOR_NEGATIVE_MEDIUM_CONNECTION.value
            edge_options['color']['highlight'] = MapColours.EDGE_HIGHLIGHT_NEGATIVE_MEDIUM_CONNECTION.value
            edge_options['width'] = 2
            sign = '-'
        elif edge.weight == ConnectionShortcode.NEGATIVE_STRONG_CONNECTION.value:
            edge_options['color']['color'] = MapColours.EDGE_COLOR_NEGATIVE_STRONG_CONNECTION.value
            edge_options['color']['highlight'] = MapColours.EDGE_HIGHLIGHT_NEGATIVE_STRONG_CONNECTION.value
            edge_options['width'] = 4
            sign = '-'

        if not edge.label:
            # edge_options['label'] = sign
            edge_options['font'] = font
    except AttributeError:
        pass

    return edge_options

def generate_legend():
    # options
    options = dict()

    arrows_to = dict()
    arrows_to['enabled'] = True
    arrows_to['scaleFactor'] = 1
    arrows_to['type'] = 'arrow'

    arrows = dict()
    arrows['to'] = arrows_to
    
    color = dict()
    color['opacity'] = 1.0

    smooth = dict()
    smooth['enabled'] = True
    smooth['type'] = 'continuous'
    smooth['roundness'] = 0.5

    edges = dict()
    edges['arrows'] = arrows
    edges['color'] = color
    edges['smooth'] = smooth

    interaction = dict()
    interaction['dragNodes'] = False
    interaction['dragView'] = False
    interaction['selectable'] = False
    interaction['selectConnectedEdges'] = False
    interaction['zoomView'] = False

    nodes = dict()
    nodes['fixed'] = True

    options['clickToUse'] = False
    options['interaction'] = interaction
    options['nodes'] = nodes
    options['edges'] = edges

    # data
    legend_structure = dict()
    nodes_data = list()
    edges_data = list()
    x = 0
    y = 0
    step_x = 185
    step_y = 85

    all_nodes = [
        NodePlus(identifier=0, label='Node', position_x=x + (0*step_x), position_y=y),
        NodePlus(identifier=1, label='Selected Node', position_x=x + (1*step_x), position_y=y),
        NodePlus(identifier=2, label='Hovered Node', position_x=x + (2*step_x), position_y=y),
        NodePlus(identifier=3, label=' '.join([ControllabilityOption.HIGH_CONTROLLABILITY.value, 'Controllability']), position_x=x + (0*step_x), position_y=y + (1*step_y), controllability=ControllabilityShortcode.HIGH_CONTROLLABILITY.value),
        NodePlus(identifier=4, label=' '.join([ControllabilityOption.MEDIUM_CONTROLLABILITY.value, 'Controllability']), position_x=x + (1*step_x), position_y=y + (1*step_y), controllability=ControllabilityShortcode.MEDIUM_CONTROLLABILITY.value),
        NodePlus(identifier=5, label=' '.join([ControllabilityOption.LOW_CONTROLLABILITY.value, 'Controllability']), position_x=x + (2*step_x), position_y=y + (1*step_y), controllability=ControllabilityShortcode.LOW_CONTROLLABILITY.value),
        NodePlus(identifier=6, label=' '.join([VulnerabilityOption.LOW_VULNERABILITY.value, 'Vulnerability']), position_x=x + (0*step_x), position_y=y + (2*step_y), vulnerability=VulnerabilityShortcode.LOW_VULNERABILITY.value),
        NodePlus(identifier=7, label=' '.join([VulnerabilityOption.MEDIUM_VULNERABILITY.value, 'Vulnerability']), position_x=x + (1*step_x), position_y=y + (2*step_y), vulnerability=VulnerabilityShortcode.MEDIUM_VULNERABILITY.value),
        NodePlus(identifier=8, label=' '.join([VulnerabilityOption.HIGH_VULNERABILITY.value, 'Vulnerability']), position_x=x + (2*step_x), position_y=y + (2*step_y), vulnerability=VulnerabilityShortcode.HIGH_VULNERABILITY.value),
        NodePlus(identifier=9, label=' '.join([ImportanceOption.LOW_IMPORTANCE.value, 'Importance']), position_x=x + (0*step_x), position_y=y + (3*step_y), importance=ImportanceShortcode.LOW_IMPORTANCE.value),
        NodePlus(identifier=10, label=' '.join([ImportanceOption.HIGH_IMPORTANCE.value, 'Importance']), position_x=x + (1*step_x), position_y=y + (3*step_y), importance=ImportanceShortcode.HIGH_IMPORTANCE.value),
        NodePlus(identifier=11, label=ConnectionOption.COMPLEX_CONNECTION.value, position_x=x + round(0.6*step_x), position_y=y + (4*step_y)),
        NodePlus(identifier=12, label='Connection', position_x=x + round(1.3*step_x), position_y=y + (4*step_y)),
        NodePlus(identifier=13, label=ConnectionOption.POSITIVE_WEAK_CONNECTION.value.split()[0], position_x=x + (0*step_x), position_y=y + (5*step_y)),
        NodePlus(identifier=14, label=ConnectionOption.POSITIVE_WEAK_CONNECTION.value.split()[1], position_x=x + round(0.75*step_x), position_y=y + (5*step_y)),
        NodePlus(identifier=15, label=ConnectionOption.POSITIVE_MEDIUM_CONNECTION.value.split()[0], position_x=x + (0*step_x), position_y=y + (6*step_y)),
        NodePlus(identifier=16, label=ConnectionOption.POSITIVE_MEDIUM_CONNECTION.value.split()[1], position_x=x + round(0.75*step_x), position_y=y + (6*step_y)),
        NodePlus(identifier=17, label=ConnectionOption.POSITIVE_STRONG_CONNECTION.value.split()[0], position_x=x + (0*step_x), position_y=y + (7*step_y)),
        NodePlus(identifier=18, label=ConnectionOption.POSITIVE_STRONG_CONNECTION.value.split()[1], position_x=x + round(0.75*step_x), position_y=y + (7*step_y)),
        NodePlus(identifier=19, label=ConnectionOption.NEGATIVE_WEAK_CONNECTION.value.split()[0], position_x=x + round(1.25*step_x), position_y=y + (5*step_y)),
        NodePlus(identifier=20, label=ConnectionOption.NEGATIVE_WEAK_CONNECTION.value.split()[1], position_x=x + (2*step_x), position_y=y + (5*step_y)),
        NodePlus(identifier=21, label=ConnectionOption.NEGATIVE_MEDIUM_CONNECTION.value.split()[0], position_x=x + round(1.25*step_x), position_y=y + (6*step_y)),
        NodePlus(identifier=22, label=ConnectionOption.NEGATIVE_MEDIUM_CONNECTION.value.split()[1], position_x=x + (2*step_x), position_y=y + (6*step_y)),
        NodePlus(identifier=23, label=ConnectionOption.NEGATIVE_STRONG_CONNECTION.value.split()[0], position_x=x + round(1.25*step_x), position_y=y + (7*step_y)),
        NodePlus(identifier=24, label=ConnectionOption.NEGATIVE_STRONG_CONNECTION.value.split()[1], position_x=x + (2*step_x), position_y=y + (7*step_y))
    ]

    all_edges =[
        EdgePlus(identifier='11-12', source=all_nodes[11], target=all_nodes[12], weight=ConnectionShortcode.COMPLEX_CONNECTION.value),
        EdgePlus(identifier='13-14', source=all_nodes[13], target=all_nodes[14], weight=ConnectionShortcode.POSITIVE_WEAK_CONNECTION.value),
        EdgePlus(identifier='15-16', source=all_nodes[15], target=all_nodes[16], weight=ConnectionShortcode.POSITIVE_MEDIUM_CONNECTION.value),
        EdgePlus(identifier='17-18', source=all_nodes[17], target=all_nodes[18], weight=ConnectionShortcode.POSITIVE_STRONG_CONNECTION.value),
        EdgePlus(identifier='19-20', source=all_nodes[19], target=all_nodes[20], weight=ConnectionShortcode.NEGATIVE_WEAK_CONNECTION.value),
        EdgePlus(identifier='21-22', source=all_nodes[21], target=all_nodes[22], weight=ConnectionShortcode.NEGATIVE_MEDIUM_CONNECTION.value),
        EdgePlus(identifier='23-24', source=all_nodes[23], target=all_nodes[24], weight=ConnectionShortcode.NEGATIVE_STRONG_CONNECTION.value)
    ]

    for node in all_nodes:
        data = node.to_json(use_dict=True)
        vis = generate_node_options(node)
        if 'Selected' in node.label:
            vis['color']['border'] = vis['color']['highlight']['border']
            vis['color']['background'] = vis['color']['highlight']['background']
        if 'Hovered' in node.label:
            vis['color']['border'] = vis['color']['hover']['border']
            vis['color']['background'] = vis['color']['hover']['background']
        nodes_data.append(dict(**data, **vis))

    for edge in all_edges:
        data = edge.to_json(use_dict=True)
        vis = generate_edge_options(edge)
        edges_data.append(dict(**data, **vis))
    
    legend_structure['nodes'] = nodes_data
    legend_structure['edges'] = edges_data

    return {'options': options, 'structure': legend_structure}
