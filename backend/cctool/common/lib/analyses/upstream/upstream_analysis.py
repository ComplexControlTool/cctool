from cctool.graphs.models.models import Edge, EdgePlus, NodePlus
from common.lib.breadth_first_search import get_bfs_tree


def find_upstream_nodes(graph, root_nodes):
    all_upstreams = dict()

    for root_node in root_nodes:
        all_upstreams = {**all_upstreams, **get_bfs_tree(graph, root_node, reverse=True, depth_limit=4)}

    return all_upstreams

def form_upstream_subgraph(graph, upstream_nodes):
    subgraph = dict()
    subgraph['nodes'] = [NodePlus.objects.get(id=node.id) for node in upstream_nodes]
    subgraph['edges'] = [EdgePlus.objects.get(id=edge.id) for node in upstream_nodes for edge in node.targets.all()]
    return subgraph
