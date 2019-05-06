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
    factor = target/raw
    for k in d:
        d[k] = d[k]*factor

def rank(d):
    sorted_by_value = sorted(d, key=d.get, reverse=True)
    d['ranked'] = sorted_by_value

def find_measurement(graph, measure='degree'):
    measurement = dict()

    nodes = graph.nodes.all().select_subclasses()
    edges = graph.edges.all().select_subclasses()

    controllability_weights = dict(zip(ControllabilityShortcode.__values__, ControllabilityWeight.__values__))
    vulnerability_weights = dict(zip(VulnerabilityShortcode.__values__, VulnerabilityWeight.__values__))
    importance_weights = dict(zip(ImportanceShortcode.__values__, ImportanceWeight.__values__))
    connection_weights = dict(zip(ConnectionShortcode.__values__, ConnectionWeight.__values__))

    G = nx.DiGraph()

    for node in nodes:
        weight = (controllability_weights[node.controllability] +
            vulnerability_weights[node.vulnerability] +
            importance_weights[node.importance])
        G.add_node(node.identifier, weight=weight)

    for edge in edges:
        weight = connection_weights[edge.weight]
        G.add_edge(edge.source.identifier, edge.target.identifier, weight=weight)

    centrality = get_centrality_measurement_nx(G, measure)
    for node_id in G.nodes:
        bfs = get_bfs_tree_nx(G, node_id, depth_limit=4)
        centrality_value = centrality.get(node_id,0)
        extra_weight = 0 
        for traversal_node_id, level in bfs.items():
            if level == 0:
                extra_weight = G.nodes.get(traversal_node_id)['weight']
                continue
            extra_weight += G.nodes.get(traversal_node_id)['weight'] / level
        measurement[node_id] = centrality_value + extra_weight

    normalize(measurement, target=10.0)
    rank(measurement)

    return measurement
