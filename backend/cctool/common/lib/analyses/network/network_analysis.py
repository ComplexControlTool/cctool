from cctool.graphs.models.models import NodePlus, EdgePlus
from cctool.common.enums import (
    ControllabilityShortcode,
    ControllabilityWeight,
    VulnerabilityShortcode,
    VulnerabilityWeight,
    ImportanceShortcode,
    ImportanceWeight,
    ConnectionShortcode,
    ConnectionWeight,
)
from cctool.common.lib.breadth_first_search import get_bfs_tree_nx
from cctool.common.lib.centralities import get_centrality_measurement_nx

import networkx as nx


def normalize(d, target=1.0):
    raw = sum(d.values())
    if raw == 0:
        return
    factor = target/raw
    for k in d:
        d[k] = d[k]*factor

def rank(d):
    sorted_by_value = sorted(d, key=d.get, reverse=True)
    d['ranked'] = sorted_by_value

def calculate_up_streams(G):
    ret = dict()
    for node_id in G.nodes:
        bfs = get_bfs_tree_nx(G, node_id, reverse=True, depth_limit=3)
        ret[node_id] = bfs
    return ret

def calculate_down_streams(G):
    ret = dict()
    for node_id in G.nodes:
        bfs = get_bfs_tree_nx(G, node_id, reverse=False, depth_limit=3)
        ret[node_id] = bfs
    return ret

def calculate_subjective_measure_stream_weight(G, subjective_measure, stream):
    weight = 0
    for traversal_node_id, level in stream.items():
        if level == 0:
            weight = G.nodes.get(traversal_node_id)[subjective_measure]
            continue
        weight += G.nodes.get(traversal_node_id)[subjective_measure] / level
    return weight

def find_measurement(G, measure='degree'):
    measurement = get_centrality_measurement_nx(G, measure)

    normalize(measurement, target=10.0)
    rank(measurement)

    return measurement

def find_subjective_measurement(G, subjective_measure, up_streams, down_streams):
    measurement = dict()

    measurement['up_stream'] = dict()
    measurement['down_stream'] = dict()
    
    for node_id in up_streams:
        measurement['up_stream'][node_id] = calculate_subjective_measure_stream_weight(G, subjective_measure, up_streams[node_id])
    for node_id in down_streams:
        measurement['down_stream'][node_id] = calculate_subjective_measure_stream_weight(G, subjective_measure, down_streams[node_id])

    normalize(measurement['up_stream'], target=10.0)
    normalize(measurement['down_stream'], target=10.0)
    rank(measurement['up_stream'])
    rank(measurement['down_stream'])

    return measurement

def find_network_analysis(graph, measures=list(), subjective_measures=list()):
    ret = dict()

    # Build graph in NetworkX
    nodes = graph.nodes.all().select_subclasses()
    edges = graph.edges.all().select_subclasses()

    controllability_weights = dict(zip(ControllabilityShortcode.__values__, ControllabilityWeight.__values__))
    vulnerability_weights = dict(zip(VulnerabilityShortcode.__values__, VulnerabilityWeight.__values__))
    importance_weights = dict(zip(ImportanceShortcode.__values__, ImportanceWeight.__values__))
    connection_weights = dict(zip(ConnectionShortcode.__values__, ConnectionWeight.__values__))

    G = nx.DiGraph()

    for node in nodes:
        controllability = controllability_weights[node.controllability]
        vulnerability = vulnerability_weights[node.vulnerability]
        importance = importance_weights[node.importance]
        G.add_node(node.identifier, controllability=controllability, vulnerability=vulnerability, importance=importance)

    for edge in edges:
        weight = connection_weights[edge.weight]
        G.add_edge(edge.source.identifier, edge.target.identifier, weight=weight)

    # Calculate all measurements given
    for measure in measures:
        ret[measure] = find_measurement(G, measure)

    # Calculate all subjective measurements given
    if subjective_measures:
        up_streams = calculate_up_streams(G)
        down_streams = calculate_down_streams(G)
    for subjective_measure in subjective_measures:
        ret[subjective_measure] = find_subjective_measurement(G, subjective_measure, up_streams, down_streams)

    return ret
