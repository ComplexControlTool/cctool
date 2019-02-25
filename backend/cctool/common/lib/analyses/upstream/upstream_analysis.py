from cctool.graphs.models.models import Edge


def get_sources(graph, node, level=0):
    sources = dict()

    def add_node(node, level):
        if not node.identifier in sources:
            sources[node.identifier] = {'node': node, 'level':level}
        return

    def get_source(graph, node, level=0, run=0):
        try:
            edges = Edge.objects.filter(graph=graph, target=node)
            level -= 1
            run += 1
            for edge in edges:
                if edge and edge.source:
                    source_node = edge.source
                    if level > 0 and source_node.identifier not in sources:
                        add_node(source_node, run)
                        get_source(graph, source_node, level, run)
                    else:
                        add_node(source_node, run)
        except Exception as e:
            pass

    add_node(node, 0)
    get_source(graph, node, level)
    return sources

def find_upstream_nodes(graph, root_nodes):
    all_upstreams = dict()

    for root_node in root_nodes:
        all_upstreams = {**all_upstreams, **get_sources(graph, root_node, level=4)}

    return all_upstreams

def form_upstream_subgraph(graph, upstream_nodes):
    subgraph = dict()
    subgraph['nodes'] = upstream_nodes
    subgraph['edges'] = [edge for node in upstream_nodes for edge in node.sources.all()]
    return subgraph
