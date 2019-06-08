from cctool.graphs.models.models import Edge, EdgePlus, NodePlus
from cctool.common.lib.breadth_first_search import get_bfs_tree


def find_downstream_nodes(graph, root_nodes):
    all_downstreams = dict()

    for root_node in root_nodes:
        all_downstreams = {**all_downstreams, **get_bfs_tree(graph, root_node, reverse=False, depth_limit=3)}

    return all_downstreams

def form_downstream_subgraph(graph, downstream_nodes):
    subgraph = dict()
    subgraph['nodes'] = [NodePlus.objects.get(id=node.id) for node in downstream_nodes]
    subgraph['edges'] = [EdgePlus.objects.get(id=edge.id) for node in downstream_nodes for edge in node.targets.all()]
    return subgraph
