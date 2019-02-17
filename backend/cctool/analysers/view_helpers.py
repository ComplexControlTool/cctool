from .tasks import find_graph_controllability
from cctool.graphs.models.models import Analysis


class AnalyserHelper:
    def analyse_graph(self, graph):
        ret = {}
        analyses = graph.analyses.all()
        for analysis in analyses:
            if analysis.analysis_type == Analysis.CONTROLLABILITY_ANALYSIS:
                func = find_graph_controllability.s(graph_id=graph.pk, analysis_id=analysis.pk)
                res = func.apply_async()
                ret['task_id'] = res.id
        return ret
