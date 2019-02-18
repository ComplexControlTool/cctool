from .tasks import find_graph_controllability
from cctool.graphs.models.models import Analysis


class AnalyserHelper:
    def analyse_graph(self, graph, analysis_type=None):
        ret = {}
        if analysis_type:
            analyses = Analysis.objects.filter(graph__id=graph.id, analysis_type=analysis_type)
        else:
            analyses = graph.analyses.all()
        for analysis in analyses:
            if analysis.analysis_type == Analysis.CONTROLLABILITY_ANALYSIS:
                func = find_graph_controllability.s(graph_id=graph.pk, analysis_id=analysis.pk)
                res = func.apply_async()
                ret['task_id'] = res.id
        return ret
