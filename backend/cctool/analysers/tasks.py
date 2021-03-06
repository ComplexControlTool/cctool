from django.core.exceptions import ObjectDoesNotExist

from cctool.common.lib.analyses.controllability import control_analysis as CA_Analysis
from cctool.common.lib.analyses.controllability import controllability_visualization as CA_Visualization
from cctool.common.lib.analyses.downstream import downstream_analysis as DSA_Analysis
from cctool.common.lib.analyses.downstream import downstream_visualization as DSA_Visualization
from cctool.common.lib.analyses.network import network_analysis as NA_Analysis
from cctool.common.lib.analyses.network import network_visualization as NA_Visualization
from cctool.common.lib.analyses.upstream import upstream_analysis as USA_Analysis
from cctool.common.lib.analyses.upstream import upstream_visualization as USA_Visualization
from cctool.graphs.models.models import Graph, Analysis, Node, NodePlus
from cctool.taskapp.celery import app as cctoolapp


@cctoolapp.task(bind=True)
def compute_controllability_analysis(self, graph_id, analysis_id):
    try:
        graph = Graph.objects.get(pk=graph_id)
    except ObjectDoesNotExist:
        raise Exception(f'Graph object with pk: {graph_id}, does not exist!')
    try:
        analysis = Analysis.objects.get(pk=analysis_id)
    except ObjectDoesNotExist:
        raise Exception(f'Analysis object with pk: {analysis_id}, does not exist!')

    nodes = graph.nodes.all().select_subclasses()
    edges = graph.edges.all().select_subclasses()
    number_of_nodes = len(nodes)

    # Analysis
    connections = dict()
    node_controllabilities = dict()
    for node in nodes:
        node_controllabilities[node.identifier] = node.controllability
        sources = node.sources.all()
        for edge in sources:
            connections.setdefault(node.identifier, set()).add(edge.target.identifier)

    analysis_data = dict()
    ranked_by_node_controllability = dict()
    
    (control_configurations, stems, frequencies) = CA_Analysis.find_controllability(connections, number_of_nodes)
    stems = {key:(dict(map(reversed,value.items()))) for (key,value) in stems.items()}
    analysis_data['controlConfigurations'] = control_configurations
    analysis_data['stems'] = stems
    analysis_data['frequencies'] = frequencies
    
    (ranked_control_configurations, ranked_stems) = CA_Analysis.rank_by_node_controllability(control_configurations, stems, node_controllabilities)
    ranked_by_node_controllability['controlConfigurations'] = ranked_control_configurations
    ranked_by_node_controllability['stems'] = ranked_stems
    analysis_data['rankedByNodeControllability'] = ranked_by_node_controllability

    analysis.data = analysis_data
    analysis.save()

    # Visualization
    graph_options = CA_Visualization.generate_graph_options()
    
    graph_structure = dict()
    nodes_data = list()
    for node in nodes:
        data = node.to_json(use_dict=True)
        vis = CA_Visualization.generate_node_options(node, analysis)
        nodes_data.append(dict(**data, **vis))
    edges_data = list()
    for edge in edges:
        data = edge.to_json(use_dict=True)
        vis = CA_Visualization.generate_edge_options(edge, analysis)
        edges_data.append(dict(**data, **vis))
    graph_structure['nodes'] = nodes_data
    graph_structure['edges'] = edges_data

    graph_legend = CA_Visualization.generate_legend()

    analysis.visualization.options = graph_options
    analysis.visualization.structure = graph_structure
    analysis.visualization.legend = graph_legend
    analysis.visualization.save()

    return

@cctoolapp.task(bind=True)
def compute_outcome_analysis(self, graph_id, analysis_id):
    try:
        graph = Graph.objects.get(pk=graph_id)
    except ObjectDoesNotExist:
        raise Exception(f'Graph object with pk: {graph_id}, does not exist!')
    try:
        analysis = Analysis.objects.get(pk=analysis_id)
    except ObjectDoesNotExist:
        raise Exception(f'Analysis object with pk: {analysis_id}, does not exist!')

    analysis_data = dict()
    graph_structure = dict()

    root_nodes = NodePlus.objects.filter(graph=graph, tags__contains='Outcome')
    analysis_data['root_nodes'] = [root_node.identifier for root_node in root_nodes]
    analysis_data['root_nodes_labels'] = [root_node.label for root_node in root_nodes]

    for root_node in root_nodes:
        root_node_analysis_data = dict()
        upstream_nodes_and_levels = USA_Analysis.find_upstream_nodes(graph, [root_node])
        upstream_nodes = [entry['node'] for entry in upstream_nodes_and_levels.values()]
        subgraph = USA_Analysis.form_upstream_subgraph(graph, upstream_nodes)
        root_node_analysis_data['root_node'] = root_node.identifier
        root_node_analysis_data['upstream_nodes_and_levels'] = {key:value['level'] for key,value in upstream_nodes_and_levels.items()}
        root_node_analysis_data['upstream_nodes'] = [node.identifier for node in upstream_nodes]
        analysis_data[root_node.identifier] = root_node_analysis_data

        root_node_graph_structure = dict()
        nodes_data = list()
        for node in subgraph['nodes']:
            data = node.to_json(use_dict=True)
            vis = USA_Visualization.generate_node_options(node, root_node_analysis_data)
            nodes_data.append(dict(**data, **vis))
        edges_data = list()
        for edge in subgraph['edges']:
            data = edge.to_json(use_dict=True)
            vis = USA_Visualization.generate_edge_options(edge, root_node_analysis_data)
            edges_data.append(dict(**data, **vis))
        root_node_graph_structure['nodes'] = nodes_data
        root_node_graph_structure['edges'] = edges_data
        graph_structure[root_node.identifier] = root_node_graph_structure

    graph_options = USA_Visualization.generate_graph_options()
    graph_legend = USA_Visualization.generate_legend()

    analysis.data = analysis_data
    analysis.save()
    analysis.visualization.options = graph_options
    analysis.visualization.structure = graph_structure
    analysis.visualization.legend = graph_legend
    analysis.visualization.save()

    return

@cctoolapp.task(bind=True)
def compute_intervention_analysis(self, graph_id, analysis_id):
    try:
        graph = Graph.objects.get(pk=graph_id)
    except ObjectDoesNotExist:
        raise Exception(f'Graph object with pk: {graph_id}, does not exist!')
    try:
        analysis = Analysis.objects.get(pk=analysis_id)
    except ObjectDoesNotExist:
        raise Exception(f'Analysis object with pk: {analysis_id}, does not exist!')

    analysis_data = dict()
    graph_structure = dict()

    root_nodes = NodePlus.objects.filter(graph=graph, tags__contains='Intervention')
    analysis_data['root_nodes'] = [root_node.identifier for root_node in root_nodes]
    analysis_data['root_nodes_labels'] = [root_node.label for root_node in root_nodes]

    for root_node in root_nodes:
        root_node_analysis_data = dict()
        downstream_nodes_and_levels = DSA_Analysis.find_downstream_nodes(graph, [root_node])
        downstream_nodes = [entry['node'] for entry in downstream_nodes_and_levels.values()]
        subgraph = DSA_Analysis.form_downstream_subgraph(graph, downstream_nodes)
        root_node_analysis_data['root_node'] = root_node.identifier
        root_node_analysis_data['downstream_nodes_and_levels'] = {key:value['level'] for key,value in downstream_nodes_and_levels.items()}
        root_node_analysis_data['downstream_nodes'] = [node.identifier for node in downstream_nodes]
        analysis_data[root_node.identifier] = root_node_analysis_data

        root_node_graph_structure = dict()
        nodes_data = list()
        for node in subgraph['nodes']:
            data = node.to_json(use_dict=True)
            vis = DSA_Visualization.generate_node_options(node, root_node_analysis_data)
            nodes_data.append(dict(**data, **vis))
        edges_data = list()
        for edge in subgraph['edges']:
            data = edge.to_json(use_dict=True)
            vis = DSA_Visualization.generate_edge_options(edge, root_node_analysis_data)
            edges_data.append(dict(**data, **vis))
        root_node_graph_structure['nodes'] = nodes_data
        root_node_graph_structure['edges'] = edges_data
        graph_structure[root_node.identifier] = root_node_graph_structure

    graph_options = DSA_Visualization.generate_graph_options()
    graph_legend = DSA_Visualization.generate_legend()

    analysis.data = analysis_data
    analysis.save()
    analysis.visualization.options = graph_options
    analysis.visualization.structure = graph_structure
    analysis.visualization.legend = graph_legend
    analysis.visualization.save()

    return

@cctoolapp.task(bind=True)
def compute_network_analysis(self, graph_id, analysis_id):
    try:
        graph = Graph.objects.get(pk=graph_id)
    except ObjectDoesNotExist:
        raise Exception(f'Graph object with pk: {graph_id}, does not exist!')
    try:
        analysis = Analysis.objects.get(pk=analysis_id)
    except ObjectDoesNotExist:
        raise Exception(f'Analysis object with pk: {analysis_id}, does not exist!')

    analysis_data = dict()
    graph_structure = dict()

    measures = ['degree', 'in-degree', 'out-degree', 'closeness', 'betweenness']
    subjective_measures = ['controllability', 'vulnerability', 'importance']
    analysis_data = NA_Analysis.find_network_analysis(graph, measures, subjective_measures)

    for measure in analysis_data:
        graph_structure[measure] = dict()
        nodes_data = list()
        for node in graph.nodes.all().select_subclasses():
            data = node.to_json(use_dict=True)
            vis = NA_Visualization.generate_node_options(node, analysis_data[measure])
            nodes_data.append(dict(**data, **vis))
        edges_data = list()
        for edge in graph.edges.all().select_subclasses():
            data = edge.to_json(use_dict=True)
            vis = NA_Visualization.generate_edge_options(edge, analysis_data[measure])
            edges_data.append(dict(**data, **vis))

        graph_structure[measure]['nodes'] = nodes_data
        graph_structure[measure]['edges'] = edges_data

    graph_options = NA_Visualization.generate_graph_options()
    graph_legend = NA_Visualization.generate_legend()

    analysis.data = analysis_data
    analysis.save()
    analysis.visualization.options = graph_options
    analysis.visualization.structure = graph_structure
    analysis.visualization.legend = graph_legend
    analysis.visualization.save()

    return

@cctoolapp.task(bind=True)
def compute_xcs_analysis(self, graph_id, analysis_id):
    graph = Graph.objects.get(pk=graph_id)
    return
