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

import networkx as nx


def find_measurement(graph, measure='degree'):
    vulnerability = dict()
    importance = dict()

    nodes = graph.nodes.all().select_subclasses()
    edges = graph.edges.all().select_subclasses()

    controllability_weights = dict(zip(ControllabilityShortcode.__values__, ControllabilityWeight.__values__))
    vulnerability_weights = dict(zip(VulnerabilityShortcode.__values__, VulnerabilityWeight.__values__))
    importance_weights = dict(zip(ImportanceShortcode.__values__, ImportanceWeight.__values__))
    connection_weights = dict(zip(ConnectionShortcode.__values__, ConnectionWeight.__values__))

    G = nx.DiGraph()

    for node in nodes:
        if measure == 'vulnerability':
            vulnerability[node.identifier] = vulnerability_weights[node.vulnerability]
        if measure == 'importance':
            importance[node.identifier] = importance_weights[node.importance]
        G.add_node(node.identifier)

    for edge in edges:
        target_node = NodePlus.objects.get(id=edge.target.id)
        controllability_weight = controllability_weights[target_node.controllability]
        vulnerability_weight = vulnerability_weights[target_node.vulnerability]
        importance_weight = importance_weights[target_node.importance]
        connection_weight = connection_weights[edge.weight]
        weight = controllability_weight + vulnerability_weight + importance_weight + connection_weight
        distance = 1/weight if weight != 0 else 1
        G.add_edge(edge.source.identifier, edge.target.identifier, weight=weight, distance=distance)

    try:
        if measure == 'degree':
            centrality = nx.degree_centrality(G)
        elif measure == 'in-degree':
            centrality = nx.in_degree_centrality(G)
        elif measure == 'out-degree':
            centrality = nx.out_degree_centrality(G)
        elif measure == 'eigenvector':
            centrality = nx.eigenvector_centrality(G)
        elif measure == 'closeness':
            centrality = nx.closeness_centrality(G)
        elif measure == 'betweenness':
            centrality = nx.betweenness_centrality(G)
        elif measure == 'vulnerability':
            centrality = vulnerability
        elif measure == 'importance':
            centrality = importance

        sorted_by_value = sorted(centrality, key=centrality.get, reverse=True)
        centrality['ranked'] = sorted_by_value
        return centrality
    except Exception as e:
        pass

    return dict()
