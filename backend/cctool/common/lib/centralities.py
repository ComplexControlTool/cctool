import networkx as nx


def get_centrality_measurement_nx(G, measure):
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

        return centrality
    except Exception as e:
        pass
        return dict()