import json
from collections import OrderedDict
from django.db.models import ForeignKey, IntegerField, CharField, CASCADE
from rest_framework.utils.encoders import JSONEncoder
from cctool.common.models import TimeStampedModel


class AbstractNode(TimeStampedModel):
    identifier = IntegerField(
        blank=False,
        default=-1,
        verbose_name='identifier of node'
    )

    label = CharField(
        blank=False,
        default='Untitled Node',
        max_length=255,
        verbose_name='label of node'
    )

    graph = ForeignKey(
        'graphs.Graph',
        on_delete=CASCADE,
        related_name='nodes',
        related_query_name='node'
    )

    class Meta:
        abstract = True
        verbose_name = 'node'
        verbose_name_plural = 'nodes'

    def __str__(self):
        graph_string = ''.join(['(', self.graph.__class__.__name__, ') ', self.graph.title])
        node_string = ''.join(['(', self.__class__.__name__, ') ', self.label])
        return ' '.join([graph_string, node_string])

    def save(self, *args, **kwargs):
        if self.identifier == -1:
            number_of_existing_nodes = self.graph.nodes.all().count()
            self.identifier = number_of_existing_nodes
        super(AbstractNode, self).save(*args, **kwargs)

    def to_json(self, dict=False, **kwargs):
        """
            Representation of Node object in Json format
        """
        output = OrderedDict((
            ('id', self.identifier),
            ('label', self.label),
        ))

        if dict:
            return output

        return json.dumps(output, cls=JSONEncoder, **kwargs)
