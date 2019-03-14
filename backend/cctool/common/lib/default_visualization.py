def generate_graph_options():
    graph_options = dict()

    arrows_to = dict()
    arrows_to['enabled'] = True
    arrows_to['scaleFactor'] = 1
    arrows_to['type'] = 'arrow'

    arrows = dict()
    arrows['to'] = arrows_to
    
    color = dict()
    color['hover'] = '#2B7CE9'
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
    highlight['border'] = '#FF3399'
    highlight['background'] = '#f1f1f1'

    hover = dict()
    hover['border'] = '#2B7CE9'
    hover['background'] = '#D2E5FF'

    color = dict()
    color['border'] = '#333'
    color['background'] = '#f1f1f1'
    color['highlight'] = highlight
    color['hover'] = hover

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

    return node_options

def generate_edge_options(edge):
    edge_options = dict()

    color = dict()
    color['color'] = '#737373'
    color['highlight'] = '#737373'

    title = list()
    try:
        title.append(f'<p>From:</p><p><strong>{edge.source.label}</strong></p><p>To:</p><p><strong>{edge.target.label}</strong></p>')
    except AttributeError:
        pass
    try:
        title.append(f'<p>Connection Weight: <strong>{edge.get_weight_display()}</strong></p>')
    except AttributeError:
        pass

    edge_options['color'] = color
    edge_options['title'] = ''.join(title)

    return edge_options
