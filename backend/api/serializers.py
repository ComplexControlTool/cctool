from rest_framework import serializers
from cctool.graphs.models import models


class GraphSerializer(serializers.ModelSerializer):
    structure = serializers.SerializerMethodField()
    analyses = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Graph
        fields = (
            'id',
            'title',
            'description',
            'created_at',
            'updated_at',
            'structure',
            'analyses',
        )

    def get_structure(self, obj):
        return obj.to_json(use_dict=True)

    def get_analyses(self, obj):
        return [analysis.to_json(use_dict=True) for analysis in obj.analyses.all()]