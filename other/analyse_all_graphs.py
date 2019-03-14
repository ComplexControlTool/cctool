from cctool.graphs.view_helpers import GraphHelper
from cctool.analysers.view_helpers import AnalyserHelper

graph_helper = GraphHelper()
analysis_helper = AnalyserHelper()

for i, graph in enumerate(Graph.objects.all()):
  print('Executing tasks on graphs...')
  graph_helper.map_graph(graph)
  graph_helper.visualize_graph(graph)
  analysis_helper.analyse_graph(graph)
  print(f'Finished graph {str(i+1)}...\n')