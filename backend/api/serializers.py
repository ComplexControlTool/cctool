from rest_framework import serializers
from cctool.graphs.models import models


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if not self.context:
            return

        # Don't pass the 'fields' arg up to the superclass
        fields = self.context['request'].query_params.get('fields', None)
        # fields = kwargs.pop('fields', None)

        if fields is not None:
            fields = fields.split(',')
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class GraphSerializer(DynamicFieldsModelSerializer):
    createdAt = serializers.DateTimeField(source='created_at')
    updatedAt = serializers.DateTimeField(source='updated_at')
    isProcessed = serializers.SerializerMethodField()
    structure = serializers.SerializerMethodField()
    visualization = serializers.SerializerMethodField()
    analysers = serializers.SerializerMethodField()
    analyses = serializers.SerializerMethodField()

    class Meta:
        model = models.Graph
        fields = (
            'id',
            'title',
            'description',
            'createdAt',
            'updatedAt',
            'isProcessed',
            'structure',
            'visualization',
            'analysers',
            'analyses',
        )

    def get_isProcessed(self, obj):
        hasStructure = False
        hasVisualization = False

        if obj.structure.data:
            hasStructure = True

        if obj.visualization.options and obj.visualization.structure:
            hasVisualization = True

        return (hasStructure and hasVisualization)

    def get_structure(self, obj):
        return obj.structure.to_json(use_dict=True)

    def get_visualization(self, obj):
        return obj.visualization.to_json(use_dict=True)

    def get_analysers(self, obj):
        return [analysis.get_analysis_type_display() for analysis in obj.analyses.all()]

    def get_analyses(self, obj):
        return [analysis.to_json(use_dict=True) for analysis in obj.analyses.all()]


class AnalyserSerializer(DynamicFieldsModelSerializer):
    isAnalysed = serializers.SerializerMethodField()
    analysis = serializers.SerializerMethodField()
    visualization = serializers.SerializerMethodField()

    class Meta:
        model = models.Graph
        fields = (
            'isAnalysed',
            'analysis',
            'visualization',
        )

    def get_isAnalysed(self, obj):
        hasData = False
        hasVisualization = False
        isUpToDate = False

        if obj.data:
            hasData = True

        if obj.visualization.options and obj.visualization.structure:
            hasVisualization = True

        if obj.updated_at > obj.graph.updated_at:
            isUpToDate = True

        return (hasData and hasVisualization and isUpToDate)

    def get_analysis(self, obj):
        ret = dict()
        ret['typeOfAnalysis'] = obj.get_analysis_type_display()
        ret['data'] = obj.data
        return ret

    def get_visualization(self, obj):
        return obj.visualization.to_json(use_dict=True)
