from django.core.management.base import BaseCommand
from django.utils import timezone

from cctool.analysers.view_helpers import AnalyserHelper
from cctool.graphs.models import Graph
from cctool.graphs.view_helpers import GraphHelper

class Command(BaseCommand):
    help = ( 
        'Performs all analysis calculations for all graphs '
        '(including mapping and visualisation).'
    )

    def handle(self, *args, **kwargs):
        graph_helper = GraphHelper()
        analysis_helper = AnalyserHelper()

        self.stdout.write(f'Executing tasks on graphs...')
        for i, graph in enumerate(Graph.objects.all()):
            self.stdout.write(f'Sending map, visualize, analyse tasks for graph {str(i+1)}: {graph.title}...')
            graph_helper.map_graph(graph)
            graph_helper.visualize_graph(graph)
            analysis_helper.analyse_graph(graph)
            self.stdout.write(f'Send taks for graph {str(i+1)}: {graph.title}...')
            break