from .tasks import compute_controllability_analysis, compute_intervention_analysis, compute_outcome_analysis, compute_network_analysis
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
                func = compute_controllability_analysis.s(graph_id=graph.pk, analysis_id=analysis.pk)
                res = func.apply_async()
                ret['task_id'] = res.id
            if analysis.analysis_type == AnalysisShortcode.INTERVENTION_ANALYSIS.value:
                func = compute_intervention_analysis.s(graph_id=graph.pk, analysis_id=analysis.pk)
                res = func.apply_async()
                ret['task_id'] = res.id
            if analysis.analysis_type == AnalysisShortcode.NETWORK_ANALYSIS.value:
                func = compute_network_analysis.s(graph_id=graph.pk, analysis_id=analysis.pk)
                res = func.apply_async()
                ret['task_id'] = res.id
            if analysis.analysis_type == AnalysisShortcode.OUTCOME_ANALYSIS.value:
                func = compute_outcome_analysis.s(graph_id=graph.pk, analysis_id=analysis.pk)
                res = func.apply_async()
                ret['task_id'] = res.id
        return ret
