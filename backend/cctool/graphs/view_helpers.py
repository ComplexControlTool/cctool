from .tasks import find_graph_map, find_graph_visualization


class GraphHelper:
    def map_graph(self, graph):
        ret = {}
        func = find_graph_map.s(graph_id=graph.pk)
        res = func.apply_async()
        ret['task_id'] = res.id
        return ret

    def visualize_graph(self, graph):
        ret = {}
        func = find_graph_visualization.s(graph_id=graph.pk)
        res = func.apply_async()
        ret['task_id'] = res.id
        return ret
