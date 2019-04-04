from cctool.graphs.models.models import NodePlus, EdgePlus

import networkx as nx


def find_measurement(graph, measure='degree'):
    centrality = dict()
    vulnerability = dict()
    importance = dict()

    nodes = graph.nodes.all().select_subclasses()
    edges = graph.edges.all().select_subclasses()

    controllability_weights = {
        NodePlus.NEUTRAL_CONTROLLABILITY: 0,
        NodePlus.EASY_CONTROLLABILITY: 1,
        NodePlus.MEDIUM_CONTROLLABILITY: 2,
        NodePlus.HARD_CONTROLLABILITY: 3
    }

    vulnerability_weights = {
        NodePlus.NO_VULNERABILITY: 0,
        NodePlus.LOW_VULNERABILITY: -1,
        NodePlus.MEDIUM_VULNERABILITY: -2,
        NodePlus.HIGH_VULNERABILITY: -3
    }

    importance_weights = {
        NodePlus.NO_IMPORTANCE: 0,
        NodePlus.LOW_IMPORTANCE: 1,
        NodePlus.HIGH_IMPORTANCE: 2
    }

    connection_weights = {
        EdgePlus.NEUTRAL_WEIGHT: 0,
        EdgePlus.POSITIVE_WEAK_WEIGHT: 1,
        EdgePlus.POSITIVE_MEDIUM_WEIGHT: 2,
        EdgePlus.POSITIVE_STRONG_WEIGHT: 3,
        EdgePlus.NEGATIVE_WEAK_WEIGHT: -1,
        EdgePlus.NEGATIVE_MEDIUM_WEIGHT: -2,
        EdgePlus.NEGATIVE_STRONG_WEIGHT: -3
    }

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
            return nx.degree_centrality(G)
        elif measure == 'in-degree':
            return nx.in_degree_centrality(G)
        elif measure == 'out-degree':
            return nx.out_degree_centrality(G)
        elif measure == 'eigenvector':
            return nx.eigenvector_centrality(G)
        elif measure == 'closeness':
            return nx.closeness_centrality(G)
        elif measure == 'betweenness':
            return nx.betweenness_centrality(G)
        elif measure == 'vulnerability':
            return vulnerability
        elif measure == 'importance':
            return importance
    except Exception as e:
        pass

    return dict()
