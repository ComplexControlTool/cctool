from cctool.common.lib import default_visualization as Visualization
from cctool.graphs.models.models import Graph
from cctool.taskapp.celery import app as cctoolapp


@cctoolapp.task(bind=True)
def find_graph_map(self, graph_id):
    graph = Graph.objects.get(pk=graph_id)
    
    structure = dict()
    structure['nodes'] = [node.to_json(use_dict=True) for node in graph.nodes.all().select_subclasses()]
    structure['edges'] = [edge.to_json(use_dict=True) for edge in graph.edges.all().select_subclasses()]
    graph.structure.data = structure
    graph.structure.save()

    return

@cctoolapp.task(bind=True)
def find_graph_visualization(self, graph_id):
    graph = Graph.objects.get(pk=graph_id)
    nodes = graph.nodes.all().select_subclasses()
    edges = graph.edges.all().select_subclasses()

    # Visualization
    graph_options = Visualization.generate_graph_options()
    graph_structure = dict()
    nodes_data = list()
    for node in nodes:
        data = node.to_json(use_dict=True)
        if 'properties' in data:
            data['cctool'] = data.pop('properties')
        vis = Visualization.generate_node_options(node)
        nodes_data.append(dict(**data, **vis))
    edges_data = list()
    for edge in edges:
        data = edge.to_json(use_dict=True)
        if 'label' in data:
            if not data.get('label'):
                data.pop('label')
        if 'source' in data:
            data['from'] = data.pop('source')
        if 'target' in data:
            data['to'] = data.pop('target')
        if 'properties' in data:
            data['cctool'] = data.pop('properties')
        vis = Visualization.generate_edge_options(edge)
        edges_data.append(dict(**data, **vis))
    graph_structure['nodes'] = nodes_data
    graph_structure['edges'] = edges_data
    graph.visualization.options = graph_options
    graph.visualization.structure = graph_structure
    graph.visualization.save()

    return

