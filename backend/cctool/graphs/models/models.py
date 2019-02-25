import json
from collections import OrderedDict
from django.db.models import CharField
from django.contrib.postgres.fields import JSONField
from model_utils.managers import InheritanceManager
from rest_framework.utils.encoders import JSONEncoder
from .graph import AbstractGraph
from .node import AbstractNode
from .edge import AbstractEdge
from .structure import AbstractStructure
from .analysis import AbstractAnalysis
from .visualization import AbstractVisualization


class Graph(AbstractGraph):

    class Meta(AbstractGraph.Meta):
        abstract = False

    def save(self, *args, **kwargs):
        if not hasattr(self, 'structure'):
            self.structure = Structure.objects.create()
        if not hasattr(self, 'visualization'):
            self.visualization = Visualization.objects.create()
        super(Graph, self).save(*args, **kwargs)


class Node(AbstractNode):
    objects = InheritanceManager()

    class Meta(AbstractNode.Meta):
        abstract = False


class Edge(AbstractEdge):
    objects = InheritanceManager()

    class Meta(AbstractEdge.Meta):
        abstract = False


class Analysis(AbstractAnalysis):

    class Meta(AbstractAnalysis.Meta):
        abstract = False

    def save(self, *args, **kwargs):
        if not hasattr(self, 'visualization'):
            self.visualization = Visualization.objects.create()
        super(Analysis, self).save(*args, **kwargs)


class Structure(AbstractStructure):

    class Meta(AbstractStructure.Meta):
        abstract = False


class Visualization(AbstractVisualization):

    class Meta(AbstractVisualization.Meta):
        abstract = False


class NodePlus(Node):
    LINEAR_FUNCTION = 'L'
    FUNCTION_SET = (
        (LINEAR_FUNCTION, 'Linear'),
    )

    NEUTRAL_CONTROLLABILITY = 'N'
    EASY_CONTROLLABILITY = 'E'
    MEDIUM_CONTROLLABILITY = 'M'
    HARD_CONTROLLABILITY = 'H'    
    CONTROLLABILITY_SET = (
        (NEUTRAL_CONTROLLABILITY, 'Neutral'),
        (EASY_CONTROLLABILITY, 'Easy'),
        (MEDIUM_CONTROLLABILITY, 'Medium'),
        (HARD_CONTROLLABILITY, 'Hard'),
    )

    NO_VULNERABILITY = 'N'
    LOW_VULNERABILITY = 'E'
    MEDIUM_VULNERABILITY = 'M'
    HIGH_VULNERABILITY = 'H'    
    VULNERABILITY_SET = (
        (NO_VULNERABILITY, 'None'),
        (LOW_VULNERABILITY, 'Low'),
        (MEDIUM_VULNERABILITY, 'Medium'),
        (HIGH_VULNERABILITY, 'High'),
    )

    NO_IMPORTANCE = 'N'
    LOW_IMPORTANCE = 'L'
    HIGH_IMPORTANCE = 'H'
    IMPORTANCE_SET = (
        (NO_IMPORTANCE, 'None'),
        (LOW_IMPORTANCE, 'Low'),
        (HIGH_IMPORTANCE, 'High'),
    )

    function = CharField(
        choices=FUNCTION_SET,
        blank=False,
        default=LINEAR_FUNCTION,
        max_length=1,
        verbose_name='node function'
    )

    controllability = CharField(
        choices=CONTROLLABILITY_SET,
        blank=False,
        default=NEUTRAL_CONTROLLABILITY,
        max_length=1,
        verbose_name='node controllability'
    )

    vulnerability = CharField(
        choices=VULNERABILITY_SET,
        blank=False,
        default=NO_VULNERABILITY,
        max_length=1,
        verbose_name='node vulnerability'
    )

    importance = CharField(
        choices=IMPORTANCE_SET,
        blank=False,
        default=NO_IMPORTANCE,
        max_length=1,
        verbose_name='node importance'
    )

    tags = JSONField(
        default=list,
        null=True,
        blank=True
    )

    custom = JSONField(
        default=dict,
        null=True,
        blank=True
    )

    def to_json(self, use_dict=False, **kwargs):
        """
            Representation of Node object in Json format
        """
        properties = dict()
        properties['function'] = self.function
        properties['controllability'] = self.controllability
        properties['vulnerability'] = self.vulnerability
        properties['importance'] = self.importance

        if self.tags:
            properties['tags'] = self.tags
        if self.custom:
            properties['custom'] = self.custom

        output = super(Node, self).to_json(use_dict=True, **kwargs)
        output['properties'] = properties

        if use_dict:
            return output

        return json.dumps(output, cls=JSONEncoder, **kwargs)


class EdgePlus(Edge):
    NEUTRAL_WEIGHT = 'N'
    POSITIVE_WEAK_WEIGHT = '+W'
    POSITIVE_MEDIUM_WEIGHT = '+M'
    POSITIVE_STRONG_WEIGHT = '+S'
    NEGATIVE_WEAK_WEIGHT = '-W'
    NEGATIVE_MEDIUM_WEIGHT = '-M'
    NEGATIVE_STRONG_WEIGHT = '-S'
    WEIGHT_SET = (
        (NEUTRAL_WEIGHT, 'Neutral'),
        (POSITIVE_WEAK_WEIGHT, 'Positive Weak'),
        (POSITIVE_MEDIUM_WEIGHT, 'Positive Medium'),
        (POSITIVE_STRONG_WEIGHT, 'Positive Strong'),
        (NEGATIVE_WEAK_WEIGHT, 'Negative Weak'),
        (NEGATIVE_MEDIUM_WEIGHT, 'Negative Medium'),
        (NEGATIVE_STRONG_WEIGHT, 'Negative Strong')
    )

    weight = CharField(
        choices=WEIGHT_SET,
        blank=False,
        default='N',
        max_length=2,
        verbose_name='edge weight'
    )

    tags = JSONField(
        default=list,
        null=True,
        blank=True
    )

    custom = JSONField(
        default=dict,
        null=True,
        blank=True
    )

    def to_json(self, use_dict=False, **kwargs):
        """
            Representation of Node object in Json format
        """
        properties = dict()
        properties['weight'] = self.weight
        
        if self.tags:
            properties['tags'] = self.tags
        if self.custom:
            properties['custom'] = self.custom
        
        output = super(Edge, self).to_json(use_dict=True, **kwargs)
        output['properties'] = properties

        if use_dict:
            return output

        return json.dumps(output, cls=JSONEncoder, **kwargs)
