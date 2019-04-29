from cctool.graphs.models.models import Edge
import networkx as nx


def get_bfs_tree(graph, source, reverse=False, depth_limit=0):
    connections = dict()

    def add_node(node, level):
        if not node.identifier in connections:
            connections[node.identifier] = {'node': node, 'level':level}
        return

    def get_connection(graph, node, reverse=False, level=0, run=0):
        try:
            if reverse:
                edges = Edge.objects.filter(graph=graph, target=node)
            else:
                edges = Edge.objects.filter(graph=graph, source=node)
            level -= 1
            run += 1
            for edge in edges:
                if reverse:
                    if not edge or not edge.source:
                        continue
                    next_node = edge.source
                else:
                    if not edge or not edge.target:
                        continue
                    next_node = edge.target
                if level > 0 and next_node.identifier not in connections:
                    add_node(next_node, run)
                    get_connection(graph, next_node, reverse, level, run)
                else:
                    add_node(next_node, run)
        except Exception as e:
            pass

    add_node(source, 0)
    get_connection(graph, source, reverse, depth_limit)
    return connections

def get_bfs_tree_nx(graph, source, reverse=False, depth_limit=0):
    connections = dict()

    nodes = graph.nodes.all().select_subclasses()
    edges = graph.edges.all().select_subclasses()

    G = nx.DiGraph()

    for node in nodes:
        G.add_node(node.identifier)

    for edge in edges:
        G.add_edge(edge.source.identifier, edge.target.identifier)

    edges = [t for (s,t) in nx.bfs_edges(G, source=source.identifier, reverse=reverse, depth_limit=depth_limit)]
    levels = nx.single_source_shortest_path_length(G,source=source.identifier, cutoff=depth_limit)

    for (node_id,level) in levels.items():
        connections[node_id] = {'node':nodes.get(identifier=node_id), 'level':level}

    return connections
