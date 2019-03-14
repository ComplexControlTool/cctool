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
        connection_string = ''.join([self.source.label, ' -> ', self.target.label])
        return ' '.join([self.label, connection_string])

    def save(self, *args, **kwargs):
        self.identifier = ''.join([str(self.source.identifier), '-', str(self.target.identifier)])
        super(AbstractEdge, self).save(*args, **kwargs)

    def to_json(self, use_dict=False, **kwargs):
        """
            Representation of Edge object in Json format
        """
        output = dict()
        output['id'] = self.identifier
        output['label'] = self.label
        output['source'] = self.source.identifier
        output['target'] = self.target.identifier

        if use_dict:
            return output

        return json.dumps(output, cls=JSONEncoder, **kwargs)
