import json
from collections import OrderedDict
from django.db.models import CharField
from model_utils.managers import InheritanceManager
from rest_framework.utils.encoders import JSONEncoder
from .graph import AbstractGraph
from .node import AbstractNode
from .edge import AbstractEdge
from .analysis import AbstractAnalysis


class Graph(AbstractGraph):

    class Meta(AbstractGraph.Meta):
        abstract = False


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


class NodeCN(Node):
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
        verbose_name='type of analysis'
    )

    controllability = CharField(
        choices=CONTROLLABILITY_SET,
        blank=False,
        default=NEUTRAL_CONTROLLABILITY,
        max_length=1,
        verbose_name='type of analysis'
    )

    importance = CharField(
        choices=IMPORTANCE_SET,
        blank=False,
        default=NO_IMPORTANCE,
        max_length=1,
        verbose_name='type of analysis'
    )

    def to_json(self, dict=False, **kwargs):
        """
            Representation of Node object in Json format
        """
        output = super(NodeCN, self).to_json(dict=True)
        properties = OrderedDict((
            ('function', self.function),
            ('controllability', self.controllability),
            ('importance', self.importance),
        ))
        output['properties'] = properties

        if dict:
            return output

        return json.dumps(output, cls=JSONEncoder, **kwargs)


class EdgeCN(Edge):
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
        verbose_name='type of analysis'
    )

    def to_json(self, dict=False, **kwargs):
        """
            Representation of Node object in Json format
        """
        output = super(EdgeCN, self).to_json(dict=True)
        properties = OrderedDict((
            ('weight', self.weight),
        ))
        output['properties'] = properties

        if dict:
            return output

        return json.dumps(output, cls=JSONEncoder, **kwargs)

