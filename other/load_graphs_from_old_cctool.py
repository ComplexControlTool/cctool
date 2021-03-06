import json
import random

from cctool.graphs.view_helpers import GraphHelper
from cctool.analysers.view_helpers import AnalyserHelper
from cctool.common.enums import (
    FunctionShortcode,
    ControllabilityShortcode,
    VulnerabilityShortcode,
    ImportanceShortcode,
    ConnectionShortcode,
)

# reference: http://cctool.co.uk/api-root/graphs/?format=json


def addGraph(title, description):
  graph_obj = Graph.objects.create(title=title, description=description)
  return graph_obj

def addNode(graph, label, function=None, controllability=None, vulnerability=None, importance=None):
  node_obj = NodePlus.objects.create(graph=graph, label=label, function=function, controllability=controllability, vulnerability=vulnerability, importance=importance)
  return node_obj

def addEdge(graph, source, target, weight=None):
  edge_obj = EdgePlus.objects.create(graph=graph, source=source, target=target, weight=weight)
  return edge_obj

def addAnalysis(graph, analysis_type):
  analysis_obj = Analysis.objects.create(graph=graph, analysis_type=analysis_type)
  return analysis_obj

def mark_nodes_as_intervention(nodes):
  repeat_times = [1,2,3]
  for i in range(random.choice(repeat_times)):
    node = random.choice(nodes)
    if 'Intervention' in node.tags:
      continue
    node.tags.append('Intervention')
    node.save()
  return

def mark_nodes_as_outcome(nodes):
  repeat_times = [1,2,3]
  for i in range(random.choice(repeat_times)):
    node = random.choice(nodes)
    if 'Outcome' in node.tags:
      continue
    node.tags.append('Outcome')
    node.save()
  return

filepath = '/Developer/cctool/other/all_graphs.json'

with open(filepath,'r') as f:
  data = json.load(f)

graph_helper = GraphHelper()
analysis_helper = AnalyserHelper()
print(f'Analysing {len(data["results"])} graphs')

for i,graph in enumerate(data['results']):
  print('Adding new graph...')
  title = graph['title']
  description = graph['description'] + '  -  with old ID: ' + str(graph['id'])
  graph_obj = addGraph(title, description)
  print(graph_obj)

  node_objs = []
  for node in graph['graphvisdatasets']['nodes']:
    label = node['label']
    vulnerability = random.choice(VulnerabilityShortcode.__values__)
    function = FunctionShortcode.LINEAR_FUNCTION.value

    controllability = node['cctool']['controllability']
    if controllability == 0:
      controllability = ControllabilityShortcode.NO_CONTROLLABILITY.value
    elif controllability.lower() == 'e':
      controllability = ControllabilityShortcode.LOW_CONTROLLABILITY.value
    elif controllability.lower() == 'm':
      controllability = ControllabilityShortcode.MEDIUM_CONTROLLABILITY.value
    elif controllability.lower() == 'h':
      controllability = ControllabilityShortcode.HIGH_CONTROLLABILITY.value
    else:
      controllability = ControllabilityShortcode.NO_CONTROLLABILITY.value

    importance = node['cctool']['importance']
    if importance == 0:
      importance = ImportanceShortcode.NO_IMPORTANCE.value
    elif importance.lower() == 'l':
      importance = ImportanceShortcode.LOW_IMPORTANCE.value
    elif importance.lower() == 'h':
      importance = ImportanceShortcode.HIGH_IMPORTANCE.value
    else:
      importance = ImportanceShortcode.NO_IMPORTANCE.value

    node_obj = addNode(graph_obj, label, function, controllability, vulnerability, importance)
    print(node_obj)
    node_objs.append(node_obj)

  for edge in graph['graphvisdatasets']['edges']:
    source = node_objs[edge['from']]
    target = node_objs[edge['to']]
    weight = edge['cctool']['weight']
    if weight == 1:
      weight = ConnectionShortcode.COMPLEX_CONNECTION.value
    elif weight.lower() == '+w':
      weight = ConnectionShortcode.POSITIVE_WEAK_CONNECTION.value
    elif weight.lower() == '+m':
      weight = ConnectionShortcode.POSITIVE_MEDIUM_CONNECTION.value
    elif weight.lower() == '+s':
      weight = ConnectionShortcode.POSITIVE_STRONG_CONNECTION.value
    elif weight.lower() == '-w':
      weight = ConnectionShortcode.NEGATIVE_WEAK_CONNECTION.value
    elif weight.lower() == '-m':
      weight = ConnectionShortcode.NEGATIVE_MEDIUM_CONNECTION.value
    elif weight.lower() == '-s':
      weight = ConnectionShortcode.NEGATIVE_STRONG_CONNECTION.value
    else:
      weight = ConnectionShortcode.COMPLEX_CONNECTION.value

    edge_obj = addEdge(graph_obj, source, target, weight)
    print(edge_obj)


  mark_nodes_as_outcome(node_objs)
  mark_nodes_as_intervention(node_objs)

  analysis_obj = addAnalysis(graph_obj, 'CA')
  analysis_obj = addAnalysis(graph_obj, 'IA')
  analysis_obj = addAnalysis(graph_obj, 'NA')
  analysis_obj = addAnalysis(graph_obj, 'OA')

  print('Executing tasks on graphs...')
  graph_helper.map_graph(graph_obj)
  graph_helper.visualize_graph(graph_obj)
  analysis_helper.analyse_graph(graph_obj)
  print(f'Finished graph {str(i+1)}...\n')
