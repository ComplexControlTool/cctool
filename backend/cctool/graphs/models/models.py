import json
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
from cctool.common.enums import (
    FunctionOption,
    FunctionShortcode,
    ControllabilityOption,
    ControllabilityShortcode,
    VulnerabilityOption,
    VulnerabilityShortcode,
    ImportanceOption,
    ImportanceShortcode,
    ConnectionOption,
    ConnectionShortcode,
)


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
    function = CharField(
        choices=list(zip(FunctionShortcode.__values__, FunctionOption.__values__)),
        blank=False,
        default=FunctionShortcode.LINEAR_FUNCTION.value,
        max_length=1,
        verbose_name='node function'
    )

    controllability = CharField(
        choices=list(zip(ControllabilityShortcode.__values__, ControllabilityOption.__values__)),
        blank=False,
        default=ControllabilityShortcode.NO_CONTROLLABILITY.value,
        max_length=1,
        verbose_name='node controllability'
    )

    vulnerability = CharField(
        choices=list(zip(VulnerabilityShortcode.__values__, VulnerabilityOption.__values__)),
        blank=False,
        default=VulnerabilityShortcode.NO_VULNERABILITY.value,
        max_length=1,
        verbose_name='node vulnerability'
    )

    importance = CharField(
        choices=list(zip(ImportanceShortcode.__values__, ImportanceOption.__values__)),
        blank=False,
        default=ImportanceShortcode.NO_IMPORTANCE.value,
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
        output['cctool'] = properties

        if use_dict:
            return output

        return json.dumps(output, cls=JSONEncoder, **kwargs)


class EdgePlus(Edge):
    weight = CharField(
        choices=list(zip(ConnectionShortcode.__values__, ConnectionOption.__values__)),
        blank=False,
        default=ConnectionShortcode.COMPLEX_CONNECTION.value,
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
        output['cctool'] = properties

        if use_dict:
            return output

        return json.dumps(output, cls=JSONEncoder, **kwargs)
