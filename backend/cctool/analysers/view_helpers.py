from .tasks import find_graph_controllability, find_downstream, find_upstream, find_subjective_logic
from cctool.graphs.models.models import Analysis
from cctool.common.enums import (
    AnalysisShortcode,
)

class AnalyserHelper:
    def analyse_graph(self, graph, analysis_type=None):
        ret = {}
        if analysis_type:
            analyses = Analysis.objects.filter(graph__id=graph.id, analysis_type=analysis_type)
        else:
            analyses = graph.analyses.all()
        for analysis in analyses:
            if analysis.analysis_type == AnalysisShortcode.CONTROLLABILITY_ANALYSIS.value:
                func = find_graph_controllability.s(graph_id=graph.pk, analysis_id=analysis.pk)
                res = func.apply_async()
                ret['task_id'] = res.id
            if analysis.analysis_type == AnalysisShortcode.DOWN_STREAM_ANALYSIS.value:
                func = find_downstream.s(graph_id=graph.pk, analysis_id=analysis.pk)
                res = func.apply_async()
                ret['task_id'] = res.id
            if analysis.analysis_type == AnalysisShortcode.UP_STREAM_ANALYSIS.value:
                func = find_upstream.s(graph_id=graph.pk, analysis_id=analysis.pk)
                res = func.apply_async()
                ret['task_id'] = res.id
            if analysis.analysis_type == AnalysisShortcode.SUBJECTIVE_LOGIC_ANALYSIS.value:
                func = find_subjective_logic.s(graph_id=graph.pk, analysis_id=analysis.pk)
                res = func.apply_async()
                ret['task_id'] = res.id
        return ret
