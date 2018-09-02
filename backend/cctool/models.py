from                 __future__ import division
from                  django.db import models
from django.contrib.auth.models import User
from        cctool.graphcontrol import Controllability


# Above the specified number in this constant,
# an approximation for control nodes will be used.
MIN_NODES_FOR_APPROXIMATION = 100;

class Graph(models.Model):
	"""
	Graph modes.
	Helps for generating objects that will be saved on our database.
	"""
	# Graph attributes (exposed to the database)
	owner            = models.ForeignKey('auth.User', related_name='graphs')
	title            = models.CharField(max_length=250)
	description      = models.CharField(max_length=500)
	moredescription  = models.TextField(max_length=1500,blank=True)
	structure        = models.TextField()
	labels           = models.TextField()
	functions        = models.TextField()
	coordinates      = models.TextField(blank=True)
	controllability  = models.TextField()
	importance       = models.TextField()
	controlconf      = models.TextField(blank=True)
	controlconfstems = models.TextField(blank=True)
	frequencies      = models.TextField(blank=True)
	dateadded        = models.DateTimeField(auto_now_add=True)
	dateupdated      = models.DateTimeField(auto_now=True)
	# Graph variables (some exposed to the REST API - check serializers.py)
	__graphanalysed            = False
	__graphconnections         = {}
	__graphstructure           = {}
	__graphnodes               = set()
	__graphnodelabels          = {}
	__graphnodefunctions       = {}
	__graphnodecoordinates     = {}
	__graphnodecontrollability = {}
	__graphnodeimportance      = {}
	__graphcontrolconf         = {}
	__graphcontrolconfstems    = []
	__graphnodefrequencies     = {}
	__graphvisdatasets         = {}
	__graphgephicsv            = ""
	__graphgephijson           = {}

	def __unicode__(self):
		return self.title

	def clear(self):
		"""
		Re-initialise Graph variables.
		"""
		self.__graphanalysed            = False
		self.__graphconnections         = {}
		self.__graphstructure           = {}
		self.__graphnodes               = set()
		self.__graphnodelabels          = {}
		self.__graphnodefunctions       = {}
		self.__graphnodecoordinates     = {}
		self.__graphnodecontrollability = {}
		self.__graphnodeimportance      = {}
		self.__graphcontrolconf         = {}
		self.__graphcontrolconfstems    = {}
		self.__graphnodefrequencies     = {}
		self.__graphvisdatasets         = {}
		self.__graphgrephicsv           = ""
		self.__graphgrephijson          = {}

		return

	def load(self):
		"""
		A function to load database attribute values into
		variables of the graph object.
		"""
		# Clear all graph's variables.
		self.clear()
		# Read in connections and structure.
		self.setConnectionsAndStructure()
		# Read in nodes and labels.
		self.setNodesAndNodeLabels()
		# Read in functions.
		self.setNodeFunctions()
		# Read in coordinates.
		self.setNodeCoordinates()
		# Read in controllability.
		self.setNodeControllability()
		# Read in importance.
		self.setNodeImportance()
		# Read in control configuration sets.
		self.setControlConf()
		# Read in control configuation stems.
		self.setControlConfStems()
		# Read in node frequencies.
		self.setNodeFrequencies()
		# Set flag if graph is analysed.
		self.isAnalysed()

		return 0

	### Setters for variables ###

	def setConnectionsAndStructure(self):
		"""
		Loop through database structure attribute,
		call addConnection method to populate
		connections/structure variables. 
		"""
		edgeFrom = 0
		for connections in self.structure.split(','):
			edgeTo = 0
			for weight in connections.split():
				if weight != '0':
					self.addConnection(edgeFrom,edgeTo,weight)
				edgeTo += 1
			edgeFrom += 1

		return 

	def setNodesAndNodeLabels(self):
		"""
		From database label attribute, generates ids (numbering)
		for the nodes variable and populates labels variable.
		"""
		node = 0
		for label in self.labels.split(','):
			self.__graphnodelabels[node] = str(label)
			self.__graphnodes = self.__graphnodes | set([node])
			node += 1

		return

	def setNodeFunctions(self):
		"""
		From database functions attribute, populate
		functions variable.
		"""
		node = 0
		for function in self.functions.split():
			self.__graphnodefunctions[node] = function
			node += 1

		return

	def setNodeCoordinates(self):
		"""
    	From database coordinates attreibute, populate
    	coordinates variable.
    	"""
		if len(self.coordinates) < 1:
			return

		node=0
		for coordinates in self.coordinates.split(','):
			if len(coordinates.split()) == 2:
				x,y = coordinates.split()
				self.__graphnodecoordinates[node] = { 'x':x, 'y':y }
			node += 1

		return

	def setNodeControllability(self):
		"""
		From database controllability attribute,
		populate controllability variable.
		"""
		node = 0
		for controllability in self.controllability.split():
			self.__graphnodecontrollability[node] = controllability
			node += 1

		return

	def setNodeImportance(self):
		"""
		From database importance attribute,
		populate importance variable.
		"""
		node = 0
		for importance in self.importance.split():
			self.__graphnodeimportance[node] = importance
			node += 1

		return

	def setControlConf(self):
		"""
		From database control configuration attribute,
		populate control configuration variable.
		"""
		line = 0
		for controlset in self.controlconf.split(','):
			self.__graphcontrolconf[line] = set( [ int(value) for value in controlset.split() ] )
			line += 1

		return

	def setControlConfStems(self):
		"""
		From database control configuration stems attribute,
		populate control configuration stems variable.
		"""
		line = 0
		for stems in self.controlconfstems.split(','):
			self.__graphcontrolconfstems[line] = {}
			for stem in stems.split():
				nodeset = stem.split(':')
				self.__graphcontrolconfstems[line][ nodeset[0] ] = nodeset[1]
			line += 1

		return

	def setNodeFrequencies(self):
		"""
		From database frequencies attribute, populate
		frequencies variable.
		"""
		# The first line determines the size of control sets.
		line = 0
		for values in self.frequencies.split(','):
			self.__graphnodefrequencies[line] = [ int(value) for value in values.split() ]
			line += 1

		return

	def setVisDataSets(self):
		"""
		From database coordinates attribute, populate
		coordinates variable
		"""
		self.__graphvisdatasets = self.generateVisDataSets()
		return

	def setGephiCSV(self):
		"""
		Using labels and structure database attributes,
		a csv that Gephi understands is generated.
		Mainly for import purposes.
		"""
		csvStructure = ""

		labels = self.labels.replace(' ','')
		labelsArr = labels.split(',')

		csvStructure += ";" + labels.replace(',',';') + "\n"
		i = 0
		for connections in self.structure.split(','):
			csvStructure += labelsArr[i] + ";" + connections.replace(' ',';').replace('-W','1').replace('+W','1').replace('-M','1').replace('+M','1').replace('-S','1').replace('+S','1') + "\n"
			i += 1

		self.__graphgephicsv = csvStructure

		return

	def setGephiJSON(self):
		"""
		Using labels and structure database attributes,
		a json that Gephi understands is generated.
		Mainly for import purposes.
		"""
		self.load()

		jsonStructure = {}
		nodes = []
		edges = []

		# Fill in nodes array
		for i in self.__graphnodes:
			nodes.append(self.generateNodeJSON(i))

		# Fill in edges array
		for i in self.__graphstructure:
			for connection in self.__graphstructure[i]:
				edgeFrom = i
				edgeTo = connection[0]
				weight = connection[1]
				edges.append(self.generateEdgeJSON(edgeFrom,edgeTo,weight))

		jsonStructure = {'nodes':nodes, 'edges':edges}

		self.__graphgephijson = jsonStructure

		return

	### Setters for model attributes ###

	def setModelControlConf(self):
		"""
		From control configuration variable,
		populate database control configuration attribute.
		"""
		line = ""
		for controlset in self.__graphcontrolconf:
			for value in self.__graphcontrolconf[controlset]:
				line += str(value) + " "
			# remove the last space of the set.
			# add comma to separate from another set.
			line = line[:-1] + ", "
		# remove the last comma and space from the generated string.
		self.controlconf = line[:-2]

		return

	def setModelControlConfStems(self):
		"""
		From control configuration stems variable,
		populate database control configuration stems attribute.
		"""
		line = ""
		for stem in self.__graphcontrolconfstems:
			for value in self.__graphcontrolconfstems[stem]:
				line += str( self.__graphcontrolconfstems[stem][value] ) + ":" + str(value) + " "
			# remove the last space of the set.
			# add comma to separate from another set.
			line = line[:-1] + ", "
		# remove the last comma and space from the generated string.
		self.controlconfstems = line[:-2]

		return

	def setModelNodeFrequencies(self):
		"""
		From frequencies variable, populate
		database frequencies attribute.
		"""
		line = ""
		for frequency in self.__graphnodefrequencies:
			for value in self.__graphnodefrequencies[frequency]:
				line += str(value) + " "
			# remove the last space of the set.
			# add comma to separate from another set.
			line = line[:-1] + ", "
		# remove the last comma and space from the generated string.
		self.frequencies = line[:-2]

		return	

	### Getters ###

	def isAnalysed(self):
		"""
		Return if the graph is analysed.
		"""
		if (self.controlconf):
			self.__graphanalysed = True
		return self.__graphanalysed

	def getConnections(self):
		"""
		Return connections variable.
		"""
		return self.__graphconnections

	def getStructure(self):
		"""
		Return structure variable
		(connections and weights).
		"""
		return self.__graphstructure

	def getNodes(self):
		"""
		Return nodes variable.
		"""
		return self.__graphnodes

	def getNodeLabels(self):
		"""
		Return labels variable.
		"""
		return self.__graphnodelabels

	def getNodeFunctions(self):
		"""
		Return functions variable.
		"""
		return self.__graphnodefunctions

	def getNodeCoordinates(self):
		"""
		Return coordinates variable.
		"""
		return self.__graphnodecoordinates

	def getNodeControllability(self):
		"""
		Return controllability variable.
		"""
		return self.__graphnodecontrollability

	def getNodeImportance(self):
		"""
		Return importance variable.
		"""
		return self.__graphnodeimportance

	def getControlConf(self):
		"""
		Return control configuration variable.
		"""
		return self.__graphcontrolconf

	def getControlConfStems(self):
		"""
		Return control configuration stems variable.
		"""
		return self.__graphcontrolconfstems

	def getNodeFrequencies(self):
		"""
		Return frequencies variable.
		"""
		return self.__graphnodefrequencies

	def getVisDataSets(self):
		"""
		Return the vis datasets variable.
		"""
		return self.__graphvisdatasets

	def getGephiCSV(self):
		"""
		Return the gephi csv variable.
		"""
		return self.__graphgephicsv

	def getGephiJSON(self):
		"""
		Return the gephi json variable.
		"""
		return self.__graphgephijson

	### Utilities ###

	def addConnection(self,edgeFrom,edgeTo,weight='1'):
		"""
		Populates graph connections/structure variables by
		adding one node at a time.
		edgeFrom: node that connections originates from.
		edgeTo: node that connection reaches.
		weight: default 1, otherwise given value.
		"""
		self.__graphconnections.setdefault(edgeFrom, set()).add(edgeTo)
		
		if edgeFrom in self.__graphstructure:
			tempList = []
			for i in self.__graphstructure[edgeFrom]:
				if i[0] != edgeTo:
					tempList.append(i)
			self.__graphstructure[edgeFrom] = tempList

		self.__graphstructure.setdefault(edgeFrom, []).append( [edgeTo,weight] )

		return

	def findControlNodes(self):
		"""
		Compute the control nodes of the graph.
		"""
		nodesNo = len(self.__graphnodes)
		# if the number of nodes exceeds the constant defined with
		# MIN_NODES_FOR_APPROXIMATION, then approximation is used
		# for efficiency.
		if (nodesNo < MIN_NODES_FOR_APPROXIMATION):
			(self.__graphcontrolconf, self.__graphcontrolconfstems) = Controllability.computeControlConf(self.__graphconnections, nodesNo)
		else:
			(self.__graphcontrolconf, self.__graphcontrolconfstems) = Controllability.computeAproxControlConf(self.__graphconnections, nodesNo)

		# Compute the frequency of the control nodes.
		if len(self.__graphcontrolconf) == 0:
			self.__graphnodefrequencies = {}
			return 0
		self.__graphnodefrequencies[0] = [ len( self.__graphcontrolconf ) ]
		self.__graphnodefrequencies[1] = [0] * nodesNo
		for i in self.__graphcontrolconf:
			for ii in self.__graphcontrolconf[i]:
				self.__graphnodefrequencies[1][ii] += 1

		return

	def sortControlNodes(self):
		"""
		Sort the control configurations
		according to the given controllability.
		"""
		(rankedControlConfs, rankedControlConfStems) = Controllability.findBestControlConf(self.__graphcontrolconf, self.__graphcontrolconfstems, self.__graphnodecontrollability)
		dSort = rankedControlConfs.keys()
		dSort.sort()

		index1 = 0
		index2 = 0
		for i in dSort:
			for confSet in rankedControlConfs[i]:
				self.__graphcontrolconf[index1] = confSet
				index1 += 1
			for confStem in rankedControlConfStems[i]:
				self.__graphcontrolconfstems[index2] = confStem
				index2 += 1

		return

	def generateAndUpdateControlNodes(self):
		"""
		Load the graph model into variables,
		find control nodes - stems - frequencies,
		sort them and then write back to the database attributes.
		"""
		self.load()

		self.findControlNodes()
		self.sortControlNodes()

		self.setModelControlConf()
		self.setModelControlConfStems()
		self.setModelNodeFrequencies()
		self.save()

		return

	def generateNodeJSON(self,i):
		"""
		Generate attributes for node visualisation purposes.
		This function will return a dictionary object with attributes/values.
		"""
		# Local variables
		nodeAttributes = {}
		nodeId = i
		nodeLabel = self.__graphnodelabels[nodeId] if nodeId in self.__graphnodelabels else str(nodeId)
		nodeCoordinates = self.__graphnodecoordinates[nodeId] if nodeId in self.__graphnodecoordinates else ""

		# Set default attributes
		nodeAttributes['id'] = nodeId
		nodeAttributes['label'] = nodeLabel

		# coordinates
		if nodeCoordinates:
			nodeAttributes['x'] = float(nodeCoordinates['x'])
			nodeAttributes['y'] = float(nodeCoordinates['y'])

		return nodeAttributes

	def generateEdgeJSON(self,edgeFrom,edgeTo,weight):
		"""
		Generate attributes for edge visualisation purposes.
		This function will return a dictionary object with attributes/values.
		"""
		# Local variables
		edgeAttributes = {}
		nodeFrom = edgeFrom
		nodeTo = edgeTo
		edgeId = str(nodeFrom) + "-" + str(nodeTo)

		# Set default attributes
		edgeAttributes['id'] = edgeId
		edgeAttributes['source'] = nodeFrom
		edgeAttributes['target'] = nodeTo

		return edgeAttributes

	def generateVisNodeValues(self,i):
		"""
		Generate attributes for node visualisation purposes.
		This function will return a dictionary object with attributes/values.
		Those values change to some properties (e.g. controllability, importance, function)
		"""
		# Local variables
		nodeAttributes = {}
		nodeId = i
		nodeLabel = self.__graphnodelabels[nodeId] if nodeId in self.__graphnodelabels else str(nodeId)
		nodeControllability = self.__graphnodecontrollability[nodeId] if nodeId in self.__graphnodecontrollability  else "0"
		nodeImportance = self.__graphnodeimportance[nodeId] if nodeId in self.__graphnodeimportance else "0"
		nodeFunction = self.__graphnodefunctions[nodeId] if nodeId in self.__graphnodefunctions else "L"
		nodeCoordinates = self.__graphnodecoordinates[nodeId] if nodeId in self.__graphnodecoordinates else ""
		nodeFrequency = 0
		if (self.isAnalysed()):
			nodeFrequency = self.__graphnodefrequencies[1][nodeId] if nodeId <= len(self.__graphnodefrequencies[1]) else "0"
		nodeCCTool = {'controllability':nodeControllability, 'importance':nodeImportance, 'function':nodeFunction }
		nodeTitle = ""

		# Set default attributes
		nodeAttributes['id'] = nodeId
		nodeAttributes['label'] = nodeLabel
		nodeAttributes['cctool'] = nodeCCTool
		nodeAttributes['borderWidth'] = 2
		nodeAttributes['borderWidthSelected'] = 2
		highlight = { 'border':'#FF3399', 'background':'#f1f1f1' }
		hover = { 'border':'#2B7CE9', 'background':'#D2E5FF' }
		nodeAttributes['color'] = { 'border':'#333', 'background':'#f1f1f1', 'highlight':highlight, 'hover':hover }
		nodeAttributes['shape'] = "ellipse"
		nodeAttributes['shapeProperties'] = { 'borderDashes':False }
		nodeAttributes['size'] = 13

		# Set Title, Attributes according to:
		if nodeLabel:
			nodeTitle += "<p><strong>"+nodeLabel+"</strong></p>"

		# coordinates
		if nodeCoordinates:
			nodeAttributes['x'] = float(nodeCoordinates['x'])
			nodeAttributes['y'] = float(nodeCoordinates['y'])

		# controllability,
		if nodeControllability =='0':
			nodeTitle += "<p>Controllability: <strong>Neutral</strong></p>"
		elif nodeControllability =='e' or nodeControllability =='E':
			nodeTitle += "<p>Controllability: <strong>Easy</strong></p>"
			highlight = { 'border':'#FF3399', 'background':'#74c476' }
			nodeAttributes['color'] = { 'border':'#238b45', 'background':'#74c476', 'highlight':highlight, 'hover':hover }
		elif nodeControllability =='m' or nodeControllability =='M':
			nodeTitle += "<p>Controllability: <strong>Medium</strong></p>"
			highlight = { 'border':'#FF3399', 'background':'#fdae6b' }
			nodeAttributes['color'] = { 'border':'#fd8d3c', 'background':'#fdae6b', 'highlight':highlight, 'hover':hover }
		elif nodeControllability =='h' or nodeControllability =='H':
			nodeTitle += "<p>Controllability: <strong>Hard</strong></p>"
			highlight = { 'border':'#FF3399', 'background':'#fb6a4a' }
			nodeAttributes['color'] = { 'border':'#cb181d', 'background':'#fb6a4a', 'highlight':highlight, 'hover':hover }

		# importance,
		if nodeImportance =='0':
			nodeTitle += "<p>Importance: <strong>None</strong></p>"
		elif nodeImportance =='l' or nodeImportance =='L':
			nodeTitle += "<p>Importance: <strong>Low</strong></p>"
			nodeAttributes['shapeProperties'] = { 'borderDashes':[2,4] }
		elif nodeImportance =='h' or nodeImportance =='H':
			nodeTitle += "<p>Importance: <strong>High</strong></p>"
			nodeAttributes['borderWidth'] = 3
			nodeAttributes['shapeProperties'] = { 'borderDashes':[15,10] }

		# functions,
		if nodeFunction =='l' or nodeFunction =='L':
			nodeTitle += "<p>Function: <strong>Linear</strong></p>"

		# frequency of control nodes.
		if nodeFrequency:
			value = 0
			defaultRadius = 13
			numberOfSets = self.__graphnodefrequencies[0][0]
			value = ( nodeFrequency / numberOfSets ) * 15
			updatedRadius = defaultRadius + value
			nodeAttributes['size'] = updatedRadius;
			nodeFrequencyPercentage = "%.0f" % ( ( nodeFrequency / numberOfSets ) * 100 )
			nodeTitle += "<p>Control Node: <strong>No</strong></p><p>Frequency: <strong>"+nodeFrequencyPercentage+"%</strong></p>"
		else:
			nodeTitle += "<p>Control Node: <strong>No</strong></p><p>Frequency: <strong>-</strong></p>"


		nodeAttributes['title'] = nodeTitle

		return nodeAttributes

	def generateVisEdgeValues(self,edgeFrom,edgeTo,weight):
		"""
		Generate attributes for edge visualisation purposes.
		This function will return a dictionary object with attributes/values.
		Those values change to some properties (e.g. weight)
		"""
		# Local variables
		edgeAttributes = {}
		nodeFrom = edgeFrom
		nodeTo = edgeTo
		nodeFromLabel = self.__graphnodelabels[nodeFrom] if nodeFrom in self.__graphnodelabels else str(nodeFrom)
		nodeToLabel = self.__graphnodelabels[nodeTo] if nodeTo in self.__graphnodelabels else str(nodeTo)
		edgeId = str(nodeFrom) + "-" + str(nodeTo)
		edgeWeight = weight
		edgeCCTool = { 'weight':edgeWeight }
		edgeTitle = ""

		# Set default attributes
		edgeAttributes['id'] = edgeId
		edgeAttributes['from'] = nodeFrom
		edgeAttributes['to'] = nodeTo
		edgeAttributes['cctool'] = edgeCCTool		
		edgeAttributes['color'] = { 'color': '#737373', 'highlight': '#737373' }

		# Set Title, Attributes according to:
		if nodeFromLabel and nodeToLabel:
			edgeTitle += "<p>From:</p><p><strong>"+nodeFromLabel+"</strong></p><p>To:</p><p><strong>"+nodeToLabel+"</strong></p>"

		# weight
		if weight == '1':
			edgeTitle += "<p>Connection Weight: <strong>Neutral</strong></p><p>Connection Influence: <strong>Neutral</strong></p>"
		elif weight == '+w' or weight == '+W':
			edgeTitle += "<p>Connection Weight: <strong>Weak</strong></p><p>Connection Influence: <strong>Positive</strong></p>"
			edgeAttributes['color'] = { 'color': '#c7e9c0', 'highlight': '#c7e9c0' }
		elif weight == '-w' or weight == '-W':
			edgeTitle += "<p>Connection Weight: <strong>Weak</strong></p><p>Connection Influence: <strong>Negative</strong></p>"
			edgeAttributes['color'] = { 'color': '#fcbba1', 'highlight': '#fcbba1' }
		elif weight == '+m' or weight == '+M':
			edgeTitle += "<p>Connection Weight: <strong>Medium</strong></p><p>Connection Influence: <strong>Positive</strong></p>"
			edgeAttributes['color'] = { 'color': '#41ab5d', 'highlight': '#41ab5d' }
		elif weight == '-m' or weight == '-M':
			edgeTitle += '<p>Connection Weight: <strong>Medium</strong></p><p>Connection Influence: <strong>Negative</strong></p>'
			edgeAttributes['color'] = { 'color': '#fb6a4a', 'highlight': '#fb6a4a' }
		elif weight == '+s' or weight == '+S':
			edgeTitle += "<p>Connection Weight: <strong>Strong</strong></p><p>Connection Influence: <strong>Positive</strong></p>"
			edgeAttributes['color'] = { 'color': '#00441b', 'highlight': '#00441b' }
		elif weight == '-s' or weight == '-S':
			edgeTitle += "<p>Connection Weight: <strong>Strong</strong></p><p>Connection Influence: <strong>Negative</strong></p>"
			edgeAttributes['color'] = { 'color': '#cb181d', 'highlight': '#cb181d' }

		edgeAttributes['title'] = edgeTitle

		return edgeAttributes

	def generateVisDataSets(self):
		"""
		Load the graph model into variables,
		convert the data into a DataSet, something
		required for the visualisation tool we are using.
		"""
		self.load()

		dataSet = {}
		nodes = []
		edges = []

		# Fill in nodes array
		for i in self.__graphnodes:
			nodes.append(self.generateVisNodeValues(i))

		# Fill in edges array
		for i in self.__graphstructure:
			for connection in self.__graphstructure[i]:
				edgeFrom = i
				edgeTo = connection[0]
				weight = connection[1]
				edges.append(self.generateVisEdgeValues(edgeFrom,edgeTo,weight))

		dataSet = {'nodes':nodes, 'edges':edges}

		return dataSet

