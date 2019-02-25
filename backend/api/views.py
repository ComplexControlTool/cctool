from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework import generics, viewsets
from rest_framework.decorators import action

from cctool.graphs.models.models import Graph, Analysis
from cctool.analysers.view_helpers import AnalyserHelper
from cctool.graphs.view_helpers import GraphHelper
from . import serializers


class GraphViewSet(viewsets.ModelViewSet):
    queryset = Graph.objects.all()
    serializer_class = serializers.GraphSerializer

    @action(detail=True)
    def map(self, request, pk=None):
        helper = GraphHelper()
        try:
            graph = Graph.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Exception(f'Graph object with pk: {pk}, does not exist!')
        result = helper.map_graph(graph)
        return JsonResponse(result)

    @action(detail=True)
    def visualize(self, request, pk=None):
        helper = GraphHelper()
        try:
            graph = Graph.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Exception(f'Graph object with pk: {pk}, does not exist!')
        result = helper.visualize_graph(graph)
        return JsonResponse(result)

    @action(detail=True)
    def analyse(self, request, pk=None):
        helper = AnalyserHelper()
        analysis_type = self.request.query_params.get('analysisType', None)
        try:
            graph = Graph.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Exception(f'Graph object with pk: {pk}, does not exist!')
        analysis_type_code = None
        if analysis_type:
            try:
                reverse_search = {v.lower(): k for k, v in Analysis.ANALYSIS_SET}
                analysis_type_code = reverse_search[analysis_type.lower()]
            except KeyError:
                pass
        result = helper.analyse_graph(graph, analysis_type_code)
        return JsonResponse(result)

class GraphAnalysisList(generics.ListAPIView):
    serializer_class = serializers.AnalyserSerializer

    def get_queryset(self):
        graph_pk = self.request.query_params.get('graphId', None)
        analysis_type = self.request.query_params.get('analysisType', None)
        if graph_pk == None or analysis_type == None:
            return {}
        try:
            reverse_search = {v.lower(): k for k, v in Analysis.ANALYSIS_SET}
            analysis_type_code = reverse_search[analysis_type.lower()]
            return Analysis.objects.filter(graph__id=graph_pk, analysis_type=analysis_type_code)
        except KeyError:
            pass
            analysis_type_code = None
            return {}
