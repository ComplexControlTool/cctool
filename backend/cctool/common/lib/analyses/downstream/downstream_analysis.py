from cctool.graphs.models.models import Edge, EdgePlus, NodePlus


def get_targets(graph, node, level=0):
    targets = dict()

    def add_node(node, level):
        if not node.identifier in targets:
            targets[node.identifier] = {'node': node, 'level':level}
        return

    def get_target(graph, node, level=0, run=0):
        try:
            edges = Edge.objects.filter(graph=graph, source=node)
            level -= 1
            run += 1
            for edge in edges:
                if edge and edge.target:
                    target_node = edge.target
                    if level > 0 and target_node.identifier not in targets:
                        add_node(target_node, run)
                        get_target(graph, target_node, level, run)
                    else:
                        add_node(target_node, run)
        except Exception as e:
            pass

    add_node(node, 0)
    get_target(graph, node, level)
    return targets

def find_downstream_nodes(graph, root_nodes):
    all_downstreams = dict()

    for root_node in root_nodes:
        all_downstreams = {**all_downstreams, **get_targets(graph, root_node, level=4)}

    return all_downstreams

def form_downstream_subgraph(graph, downstream_nodes):
    subgraph = dict()
    subgraph['nodes'] = [NodePlus.objects.get(id=node.id) for node in downstream_nodes]
    subgraph['edges'] = [EdgePlus.objects.get(id=edge.id) for node in downstream_nodes for edge in node.targets.all()]
    return subgraph
