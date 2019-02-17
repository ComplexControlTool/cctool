from cctool.common.lib.analyses.controllability import controllability_analysis as CA_Analysis
from cctool.common.lib.analyses.controllability import controllability_visualization as CA_Visualization
from cctool.graphs.models.models import Graph, Analysis
from cctool.taskapp.celery import app as cctoolapp


@cctoolapp.task(bind=True)
def find_graph_controllability(self, graph_id, analysis_id):
    graph = Graph.objects.get(pk=graph_id)
    analysis = Analysis.objects.get(pk=analysis_id)
    nodes = graph.nodes.all().select_subclasses()
    edges = graph.edges.all().select_subclasses()
    number_of_nodes = len(nodes)

    # Analysis
    connections = dict()
    for node in nodes:
        sources = node.sources.all()
        for edge in sources:
            connections.setdefault(node.identifier, set()).add(edge.target.identifier)

    # TODO: Need to calculate frequencies + best configurations - ordered
    (control_configurations, stems) = CA_Analysis.computeControlConf(connections, number_of_nodes)
    analysis_data = dict()
    analysis_data['controlConfigurations'] = control_configurations
    analysis_data['stems'] = stems
    analysis.data = analysis_data
    analysis.save()

    # Visualization
    graph_options = CA_Visualization.generate_graph_options()
    graph_structure = dict()
    nodes_data = list()
    for node in nodes:
        data = node.to_json(use_dict=True)
        if 'properties' in data:
            data['cctool'] = data.pop('properties')
        vis = CA_Visualization.generate_node_options(node, analysis)
        nodes_data.append(dict(**data, **vis))
    edges_data = list()
    for edge in edges:
        data = edge.to_json(use_dict=True)
        if 'source' in data:
            data['from'] = data.pop('source')
        if 'target' in data:
            data['to'] = data.pop('target')
        if 'properties' in data:
            data['cctool'] = data.pop('properties')
        vis = CA_Visualization.generate_edge_options(edge, analysis)
        edges_data.append(dict(**data, **vis))
    graph_structure['nodes'] = nodes_data
    graph_structure['edges'] = edges_data
    analysis.visualization.options = graph_options
    analysis.visualization.structure = graph_structure
    analysis.visualization.save()

    return

@cctoolapp.task(bind=True)
def find_up_stream(self, graph_id):
    graph = Graph.objects.get(pk=graph_id)
    return

@cctoolapp.task(bind=True)
def find_down_stream(self, graph_id):
    graph = Graph.objects.get(pk=graph_id)
    return

@cctoolapp.task(bind=True)
def find_subjective_logic(self, graph_id):
    graph = Graph.objects.get(pk=graph_id)
    return

@cctoolapp.task(bind=True)
def find_xcs_classifier(self, graph_id):
    graph = Graph.objects.get(pk=graph_id)
    return