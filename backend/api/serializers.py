from rest_framework import serializers
from cctool.graphs.models import models
from cctool.common.enums import *
from cctool.graphs.view_helpers import GraphHelper
from cctool.analysers.view_helpers import AnalyserHelper


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


class AnalysisSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        analysis_type = data

        if not analysis_type:
            raise serializers.ValidationError({
                'analysis_type': 'This field is required.'
            })
        if analysis_type not in AnalysisShortcode.__values__:
            raise serializers.ValidationError({
                'analysis_type': 'The specified value is not supported.'
            })

        return analysis_type


class NodeSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        ret = dict()
        identifier = data.get('id', '-1')
        label = data.get('label', 'Untitled Node')
        position_x = data.get('x', None)
        position_y = data.get('y', None)
        cctool = data.get('cctool', dict())
        validated_node_plus = dict()

        if not label:
            raise serializers.ValidationError({
                'label': 'This field is required.'
            })
        if len(label) > 255:
            raise serializers.ValidationError({
                'label': 'This field is limited to 255 characters.'
            })

        if cctool:
            node_plus_serializer = NodePlusSerializer(data=cctool)
            if not node_plus_serializer.is_valid():
                raise serializers.ValidationError({
                    'cctool': 'Data in cctool are not valid.'
                })
            validated_node_plus = node_plus_serializer.validated_data
            if validated_node_plus:
                ret['cctool'] = validated_node_plus

        ret['identifier'] = identifier
        ret['label'] = label
        ret['position_x'] = position_x
        ret['position_y'] = position_y

        return ret


class NodePlusSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        ret = dict()
        function = data.get('function', FunctionShortcode.LINEAR_FUNCTION.value)
        controllability = data.get('controllability', ControllabilityShortcode.NO_CONTROLLABILITY.value)
        vulnerability = data.get('vulnerability', VulnerabilityShortcode.NO_VULNERABILITY.value)
        importance = data.get('importance', ImportanceShortcode.NO_IMPORTANCE.value)
        tags = data.get('tags', list())
        custom = data.get('custom', dict())

        if not function:
            raise serializers.ValidationError({
                'function': 'This field is required.'
            })
        if not controllability:
            raise serializers.ValidationError({
                'controllability': 'This field is required.'
            })
        if not vulnerability:
            raise serializers.ValidationError({
                'vulnerability': 'This field is required.'
            })
        if not importance:
            raise serializers.ValidationError({
                'importance': 'This field is required.'
            })

        if function not in FunctionShortcode.__values__:
            raise serializers.ValidationError({
                'function': 'The specified value is not supported.'
            })
        if controllability not in ControllabilityShortcode.__values__:
            raise serializers.ValidationError({
                'function': 'The specified value is not supported.'
            })
        if vulnerability not in VulnerabilityShortcode.__values__:
            raise serializers.ValidationError({
                'function': 'The specified value is not supported.'
            })
        if importance not in ImportanceShortcode.__values__:
            raise serializers.ValidationError({
                'function': 'The specified value is not supported.'
            })
        if not isinstance(tags, list):
            raise serializers.ValidationError({
                'tags': 'This field should be of a list type.'
            })
        if not isinstance(custom, dict):
            raise serializers.ValidationError({
                'custom': 'This field should be of a dict type.'
            })

        ret['function'] = function
        ret['controllability'] = controllability
        ret['vulnerability'] = vulnerability
        ret['importance'] = importance
        ret['tags'] = tags
        ret['custom'] = custom

        return ret


class EdgeSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        ret = dict()
        identifier = data.get('id', '-1')
        label = data.get('label', '')
        source = data.get('from', None)
        target = data.get('to', None)
        cctool = data.get('cctool', dict())
        validated_edge_plus = dict()

        if source == None or target == None:
            raise serializers.ValidationError({
                'to/from': 'These fields are required.'
            })
        if label and len(label) > 255:
            raise serializers.ValidationError({
                'label': 'This field is limited to 255 characters.'
            })
        if cctool:
            edge_plus_serializer = EdgePlusSerializer(data=cctool)
            if not edge_plus_serializer.is_valid():
                raise serializers.ValidationError({
                    'cctool': 'Data in cctool are not valid.'
                })
            validated_edge_plus = edge_plus_serializer.validated_data
            if validated_edge_plus:
                ret['cctool'] = validated_edge_plus

        ret['identifier'] = identifier
        ret['label'] = label
        ret['from'] = source
        ret['to'] = target

        return ret


class EdgePlusSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        ret = dict()
        weight = data.get('weight', ConnectionShortcode.COMPLEX_CONNECTION.value)
        tags = data.get('tags', list())
        custom = data.get('custom', dict())

        if not weight:
            raise serializers.ValidationError({
                'weight': 'This field is required.'
            })

        if weight not in ConnectionShortcode.__values__:
            raise serializers.ValidationError({
                'weight': 'The specified value is not supported.'
            })
        if not isinstance(tags, list):
            raise serializers.ValidationError({
                'tags': 'This field should be of a list type.'
            })
        if not isinstance(custom, dict):
            raise serializers.ValidationError({
                'custom': 'This field should be of a dict type.'
            })

        ret['weight'] = weight
        ret['tags'] = tags
        ret['custom'] = custom

        return ret


class GraphSerializer(serializers.BaseSerializer):
    def clear_structure_and_analysis(self, graph_object):
        graph_object.nodes.all().delete()
        graph_object.edges.all().delete()
        graph_object.analyses.all().delete()
        
        # Assign new empty structure and visualization objects
        structure_to_delete = graph_object.structure
        visualization_to_delete = graph_object.visualization
        graph_object.structure = models.Structure.objects.create()
        graph_object.visualization = models.Visualization.objects.create()
        structure_to_delete.delete()
        visualization_to_delete.delete()
        return

    def set_analyses(self, graph_object, analysis_data):
        if analysis_data:
            for analysis_type in analysis_data:
                temp = models.Analysis.objects.create(graph=graph_object, analysis_type=analysis_type)
        analysis_helper = AnalyserHelper()
        analysis_helper.analyse_graph(graph_object)
        return

    def set_structure(self, graph_object, structure_data):
        if structure_data:
            edges = structure_data.get('edges', dict())
            nodes = structure_data.get('nodes', dict())

            created_nodes = dict()
            for node_data in nodes:
                if 'cctool' in node_data:
                    cctool_data = node_data.pop('cctool')
                    temp = models.NodePlus.objects.create(graph=graph_object, **node_data, **cctool_data)
                else:
                    temp = models.Node.objects.create(graph=graph_object, **node_data)
                created_nodes[temp.identifier] = temp
            for edge_data in edges:
                try:
                    source = created_nodes[edge_data.pop('from')]
                    target = created_nodes[edge_data.pop('to')]
                    if 'cctool' in edge_data:
                        cctool_data = edge_data.pop('cctool')
                        temp = models.EdgePlus.objects.create(graph=graph_object, source=source, target=target, **edge_data, **cctool_data)
                    else:
                        temp = models.Edge.objects.create(graph=graph_object, source=source, target=target, **edge_data)
                except IndexError:
                    pass
            graph_helper = GraphHelper()
            graph_helper.map_graph(graph_object)
            graph_helper.visualize_graph(graph_object)

    def get_id(self, obj):
        return obj.id

    def get_title(self, obj):
        return obj.title

    def get_description(self, obj):
        return obj.description

    def get_createdAt(self, obj):
        return obj.created_at

    def get_updatedAt(self, obj):
        return obj.updated_at

    def get_isProcessed(self, obj):
        hasStructure = False
        hasVisualization = False
        isUpToDate = False

        if obj.structure.data:
            hasStructure = True

        if obj.visualization.options and obj.visualization.structure:
            hasVisualization = True

        if obj.structure.updated_at >= obj.updated_at and obj.visualization.updated_at >= obj.updated_at:
            isUpToDate = True

        return (hasStructure and hasVisualization and isUpToDate)

    def get_structure(self, obj):
        return obj.structure.to_json(use_dict=True)

    def get_visualization(self, obj):
        return obj.visualization.to_json(use_dict=True)

    def get_analysers(self, obj):
        default_description = 'No description available yet!'
        analyses_descriptions = dict(zip(AnalysisOption.__values__, AnalysisDescription.__values__))
        available_analysis = obj.analyses.all()

        ret = dict()
        for analysis in available_analysis:
            name = analysis.get_analysis_type_display()
            ret[name] = analyses_descriptions.get(name, default_description)

        return ret

    def get_analyses(self, obj):
        return [analysis.to_json(use_dict=True) for analysis in obj.analyses.all()]

    def get_analysisTypes(self, obj):
        return [analysis.analysis_type for analysis in obj.analyses.all()]

    def to_internal_value(self, data):
        ret = dict()
        title = data.get('title', None)
        description = data.get('description', '')
        structure = data.get('structure', dict())
        analysis_types = data.get('analysisTypes', list())
        validated_structure = dict()
        validated_analysis_types = list()

        if not title:
            raise serializers.ValidationError({
                'title': 'This field is required.'
            })
        if len(title) > 255:
            raise serializers.ValidationError({
                'title': 'This field is limited to 255 characters.'
            })
        if description and len(description) > 1500:
            raise serializers.ValidationError({
                'title': 'This field is limited to 1500 characters.'
            })
        if structure:
            edges = structure.get('edges', dict())
            nodes = structure.get('nodes', dict())

            nodes_serializer = NodeSerializer(many=True, data=nodes)
            if not nodes_serializer.is_valid():
                raise serializers.ValidationError({
                    'nodes': 'Nodes in structure are not valid.'
                })
            edges_serializer = EdgeSerializer(many=True, data=edges)
            if not edges_serializer.is_valid():
                raise serializers.ValidationError({
                    'edges': 'Edges in structure are not valid.'
                })
            validated_structure = {'nodes': nodes_serializer.validated_data, 'edges': edges_serializer.validated_data}
        if analysis_types:
            analysis_serializer = AnalysisSerializer(many=True, data=analysis_types)
            if not analysis_serializer.is_valid():
                raise serializers.ValidationError({
                    'analysisTypes': 'Analysis Types are not valid.'
                })
            validated_analysis_types = analysis_serializer.validated_data

        return {
            'title': title,
            'description': description,
            'structure': validated_structure,
            'analysisTypes': validated_analysis_types 
        }

    def to_representation(self, obj):
        # Ability to restrict on specified fields
        ret = dict()
        allowed_fields = (
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
            'analysisTypes',
        )
        fields = self.context['request'].query_params.get('fields', ','.join(allowed_fields)).split(',')
        for field_name in fields:
            method_name = 'get_{field_name}'.format(field_name=field_name)
            if field_name in allowed_fields:
                ret[field_name] = getattr(self,method_name)(obj)
        return ret

    def create(self, validated_data):
        structure = validated_data.pop('structure')
        analysis_types = validated_data.pop('analysisTypes')
        graph = models.Graph.objects.create(**validated_data)
        self.set_structure(graph, structure)
        self.set_analyses(graph, analysis_types)
        return graph

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        self.clear_structure_and_analysis(instance)
        instance.save()
        self.set_structure(instance, validated_data.get('structure', dict()))
        self.set_analyses(instance, validated_data.get('analysisTypes', list()))
        return instance


class AnalyserSerializer(DynamicFieldsModelSerializer):
    updatedAt = serializers.DateTimeField(source='updated_at')
    isAnalysed = serializers.SerializerMethodField()
    analysis = serializers.SerializerMethodField()
    visualization = serializers.SerializerMethodField()

    class Meta:
        model = models.Graph
        fields = (
            'updatedAt',
            'isAnalysed',
            'analysis',
            'visualization',
        )
        read_only_fields = (
            'updatedAt',
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

        if obj.updated_at >= obj.graph.updated_at:
            isUpToDate = True

        return (hasData and hasVisualization and isUpToDate)

    def get_analysis(self, obj):
        ret = dict()
        ret['typeOfAnalysis'] = obj.get_analysis_type_display()
        ret['data'] = obj.data
        return ret

    def get_visualization(self, obj):
        return obj.visualization.to_json(use_dict=True)
