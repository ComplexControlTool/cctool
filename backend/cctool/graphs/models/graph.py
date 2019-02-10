import json
from collections import OrderedDict
from django.db.models import ForeignKey, CharField, TextField, CASCADE
from rest_framework.utils.encoders import JSONEncoder
from cctool.common.models import TimeStampedModel


class AbstractGraph(TimeStampedModel):
    title = CharField(
        blank=False,
        default='Untitled Graph',
        max_length=255,
        verbose_name='title of graph'
    )

    description = TextField(
        blank=True,
        max_length=1500,
        verbose_name='description of graph'
    )

    class Meta:
        abstract = True
        verbose_name = 'graph'
        verbose_name_plural = 'graphs'

    def __str__(self):
        graph_string = ''.join(['(', self.__class__.__name__, ') ', self.title])
        return graph_string

    def to_json(self, use_dict=False, **kwargs):
        """
            Representation of Graph object in Json format
        """
        output = OrderedDict((
            ('nodes', [node.to_json(use_dict=use_dict, **kwargs) for node in self.nodes.all().select_subclasses()]),
            ('edges', [edge.to_json(use_dict=use_dict, **kwargs) for edge in self.edges.all().select_subclasses()]),
        ))

        if use_dict:
            return output

        return json.dumps(output, cls=JSONEncoder, **kwargs)
