import json
from collections import OrderedDict
from django.db.models import ForeignKey, CharField, CASCADE
from rest_framework.utils.encoders import JSONEncoder
from cctool.common.models import TimeStampedModel


class AbstractEdge(TimeStampedModel):
    identifier = CharField(
        blank=False,
        default='0-0',
        max_length=21,
        verbose_name='identifier of edge'
    )

    label = CharField(
        blank=True,
        max_length=255,
        verbose_name='label of edge'
    )

    source = ForeignKey(
        'graphs.Node',
        on_delete=CASCADE,
        related_name='sources',
        related_query_name='source'
    )

    target = ForeignKey(
        'graphs.Node',
        on_delete=CASCADE,
        related_name='targets',
        related_query_name='target'
    )

    graph = ForeignKey(
        'graphs.Graph',
        on_delete=CASCADE,
        related_name='edges',
        related_query_name='edge'
    )

    class Meta:
        abstract = True
        verbose_name = 'edge'
        verbose_name_plural = 'edges'

    def __str__(self):
        graph_string = ''.join(['(', self.graph.__class__.__name__, ') ', self.graph.title])
        edge_string = ''.join(['(', self.__class__.__name__, ') ', self.label])
        connection_string = ''.join([self.source.label, ' -> ', self.target.label])
        return ' '.join([graph_string, edge_string, connection_string])

    def save(self, *args, **kwargs):
        super(AbstractEdge, self).save(*args, **kwargs)
        self.identifier = ''.join([str(self.source.identifier), '-', str(self.target.identifier)])

    def to_json(self, dict=False, **kwargs):
        """
            Representation of Edge object in Json format
        """
        output = OrderedDict((
            ('id', self.identifier),
            ('label', self.label),
            ('source', self.source.identifier),
            ('target', self.target.identifier),
        ))

        if dict:
            return output

        return json.dumps(output, cls=JSONEncoder, **kwargs)
