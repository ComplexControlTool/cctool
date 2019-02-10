from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from cctool.graphs.models.models import Graph
from cctool.analysers.view_helpers import AnalyserHelper
from . import serializers


class GraphViewSet(viewsets.ModelViewSet):
    queryset = Graph.objects.all()
    serializer_class = serializers.GraphSerializer

    @action(detail=True)
    def analyse(self, request, pk=None):
        helper = AnalyserHelper()
        try:
            graph = Graph.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Exception(f'Graph object with pk: {pk}, does not exist!')
        result = helper.analyse_graph(graph)
        return JsonResponse(result)