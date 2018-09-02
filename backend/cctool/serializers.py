from django.contrib.auth.models import User
from              cctool.models import Graph
from             rest_framework import serializers


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


class GraphSerializer(DynamicFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
	owner                    = serializers.ReadOnlyField(source='owner.username')
	graphanalysed            = serializers.SerializerMethodField('is_graph_analysed')
	graphconnections         = serializers.SerializerMethodField('load_graphconnections')
	graphstructure           = serializers.SerializerMethodField('load_graphstructure')
	graphnodes               = serializers.SerializerMethodField('load_graphnodes')
	graphnodelabels          = serializers.SerializerMethodField('load_graphnodelabels')
	graphnodefunctions       = serializers.SerializerMethodField('load_graphnodefunctions')
	graphnodecoordinates     = serializers.SerializerMethodField('load_graphnodecoordinates')
	graphnodecontrollability = serializers.SerializerMethodField('load_graphnodecontrollability')
	graphnodeimportance      = serializers.SerializerMethodField('load_graphnodeimportance')
	graphcontrolconf         = serializers.SerializerMethodField('load_graphcontrolconf')
	graphcontrolconfstems    = serializers.SerializerMethodField('load_graphcontrolconfstems')
	graphnodefrequencies     = serializers.SerializerMethodField('load_graphnodefrequencies')
	graphvisdatasets         = serializers.SerializerMethodField('load_graphvisdatasets')
	graphgephicsv            = serializers.SerializerMethodField('load_graphgephicsv')
	graphgephijson           = serializers.SerializerMethodField('load_graphgephijson')

	class Meta:
		model  = Graph
		fields = ('id',
				  'url',
				  'owner',
				  'title',
				  'description',
				  'moredescription',
				  'structure', 
				  'labels',
				  'functions',
				  'coordinates',
				  'controllability',
				  'importance',
				  'controlconf',
				  'controlconfstems',
				  'frequencies',
				  'dateadded',
				  'dateupdated',

				  'graphanalysed',
				  'graphconnections',
				  'graphstructure',
				  'graphnodes',
				  'graphnodelabels',
				  'graphnodefunctions',
				  'graphnodecoordinates',
				  'graphnodecontrollability',
				  'graphnodeimportance',
				  'graphcontrolconf',
				  'graphcontrolconfstems',
				  'graphnodefrequencies',
				  'graphvisdatasets',
				  'graphgephicsv',
				  'graphgephijson')

	def is_graph_analysed(self, obj):
		obj.clear()
		obj.load()
		return obj.isAnalysed()
	def load_graphconnections(self, obj):
		obj.clear()
		obj.setConnectionsAndStructure()
		return obj.getConnections()
	def load_graphstructure(self, obj):
		obj.clear()
		obj.setConnectionsAndStructure()
		return obj.getStructure()
	def load_graphnodes(self, obj):
		obj.clear()
		obj.setNodesAndNodeLabels()
		return obj.getNodes()
	def load_graphnodelabels(self, obj):
		obj.clear()
		obj.setNodesAndNodeLabels()
		return obj.getNodeLabels()
	def load_graphnodefunctions(self, obj):
		obj.clear()
		obj.setNodeFunctions()
		return obj.getNodeFunctions()
	def load_graphnodecoordinates(self, obj):
		obj.clear()
		obj.setNodeCoordinates()
		return obj.getNodeCoordinates()
	def load_graphnodecontrollability(self, obj):
		obj.clear()
		obj.setNodeControllability()
		return obj.getNodeControllability()
	def load_graphnodeimportance(self, obj):
		obj.clear()
		obj.setNodeImportance()
		return obj.getNodeImportance()
	def load_graphcontrolconf(self, obj):
		obj.clear()
		obj.setControlConf()
		return obj.getControlConf()
	def load_graphcontrolconfstems(self, obj):
		obj.clear()
		obj.setControlConfStems()
		return obj.getControlConfStems()
	def load_graphnodefrequencies(self, obj):
		obj.clear()
		obj.setNodeFrequencies()
		return obj.getNodeFrequencies()
	def load_graphvisdatasets(self, obj):
		obj.clear()
		obj.setVisDataSets()
		return obj.getVisDataSets()
	def load_graphgephicsv(self, obj):
		obj.clear()
		obj.setGephiCSV()
		return obj.getGephiCSV()
	def load_graphgephijson(self, obj):
		obj.clear()
		obj.setGephiJSON()
		return obj.getGephiJSON()

class UserSerializer(DynamicFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
	queryset = Graph.objects.all()
	graphs = GraphSerializer(queryset, many=True)

	class Meta:
		model  = User
		fields = ('id', 'url', 'username', 'graphs')

class ImplicationsSerializer(DynamicFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
	owner             = serializers.ReadOnlyField(source='owner.username')
	graphimplications = serializers.SerializerMethodField('generate_implications')

	class Meta:
		model  = Graph
		fields = ('id', 'url', 'owner', 'graphimplications')

	def generate_implications(self, obj):
		obj.generateAndUpdateControlNodes()
		return 1

