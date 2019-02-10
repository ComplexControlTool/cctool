from cctool.common.lib.analyses.controllability import controllability_analysis as CA_Analysis
from cctool.common.lib.analyses.controllability import controllability_visualization as CA_Visualization
from cctool.graphs.models.models import Graph, Analysis
from cctool.taskapp.celery import app as cctoolapp


@cctoolapp.task(bind=True)
def find_graph_controllability(self, graph_id, analysis_id):
    graph = Graph.objects.get(pk=graph_id)
    analysis = Analysis.objects.get(pk=analysis_id)
    nodes = graph.nodes.all()
    number_of_nodes = len(nodes)

    connections = dict()
    for node in nodes:
        sources = node.sources.all()
        for edge in sources:
            connections.setdefault(node.identifier, set()).add(edge.target.identifier)

    (control_configurations, stems) = CA_Analysis.computeControlConf(connections, number_of_nodes)
    analysis_data = dict()
    analysis_data['controlConfigurations'] = control_configurations
    analysis_data['stems'] = stems
    analysis.analysis_data = analysis_data
    analysis.save()

    network_visualization = CA_Visualization.generate_graph_options()
    analysis.visualization.options = network_visualization
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