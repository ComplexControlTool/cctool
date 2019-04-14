from cctool.common.enums import (
    ControllabilityShortcode,
    VulnerabilityShortcode,
    ImportanceShortcode,
    ConnectionShortcode,
    MapColours,
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

    layout = dict()
    layout['randomSeed'] = 2

    interaction = dict()
    interaction['hover'] = True
    interaction['navigationButtons'] = True

    physics = dict()
    physics['enabled'] = False

    graph_options['autoResize'] = True
    graph_options['width'] = '100%'
    graph_options['height'] = '100%'
    graph_options['locale'] = 'en'
    graph_options['clickToUse'] = True
    graph_options['edges'] = edges
    graph_options['layout'] = layout
    graph_options['interaction'] = interaction
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
        if node.position_x:
            node_options['x'] = position_x
    except AttributeError:
        pass
    try:
        if node.position_y:
            node_options['y'] = position_y
    except AttributeError:
        pass

    # Define specifics for attributes: Controllability, Vulnerability, Importance
    shadow = dict()
    shadow['enabled'] = True

    # Controllability
    try:
        if node.controllability == ControllabilityShortcode.EASY_CONTROLLABILITY.value:
            node_options['color']['highlight']['border'] = MapColours.NODE_HIGHLIGHT_BORDER_EASY_CONTROLLABILITY.value
            node_options['color']['border'] = MapColours.NODE_BORDER_EASY_CONTROLLABILITY.value
        elif node.controllability == ControllabilityShortcode.MEDIUM_CONTROLLABILITY.value:
            node_options['color']['highlight']['border'] = MapColours.NODE_HIGHLIGHT_BORDER_MEDIUM_CONTROLLABILITY.value
            node_options['color']['border'] = MapColours.NODE_BORDER_MEDIUM_CONTROLLABILITY.value
        elif node.controllability == ControllabilityShortcode.HARD_CONTROLLABILITY.value:
            node_options['color']['highlight']['border'] = MapColours.NODE_HIGHLIGHT_BORDER_HARD_CONTROLLABILITY.value
            node_options['color']['border'] = MapColours.NODE_BORDER_HARD_CONTROLLABILITY.value
    except AttributeError:
        pass

    # Vulnerability
    try:
        if node.vulnerability == VulnerabilityShortcode.LOW_VULNERABILITY.value:
            node_options['shapeProperties']['borderDashes'] = [2,3]
        elif node.vulnerability == VulnerabilityShortcode.MEDIUM_VULNERABILITY.value:
            node_options['shapeProperties']['borderDashes'] = [4,6]
        elif node.vulnerability == VulnerabilityShortcode.HIGH_VULNERABILITY.value:
            node_options['shapeProperties']['borderDashes'] = [8,12]
    except AttributeError:
        pass

    # Importance
    try:
        if node.importance == ImportanceShortcode.LOW_IMPORTANCE.value:
            node_options['color']['background'] = MapColours.NODE_BACKGROUND_LOW_IMPORTANCE.value
            node_options['shadow'] = shadow
        elif node.importance == ImportanceShortcode.HIGH_IMPORTANCE.value:
            node_options['color']['background'] = MapColours.NODE_BACKGROUND_HIGH_IMPORTANCE.value
            node_options['shadow'] = shadow
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
            edge_options['label'] = sign
            edge_options['font'] = font
    except AttributeError:
        pass

    return edge_options

