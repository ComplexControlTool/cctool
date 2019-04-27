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

    position_x = IntegerField(
        blank=True,
        null=True,
        default=None,
        verbose_name='position on x-axis of node'
    )

    position_y = IntegerField(
        blank=True,
        null=True,
        default=None,
        verbose_name='position on y-axis of node'
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
        return self.label

    def save(self, *args, **kwargs):
        if self.identifier == -1:
            number_of_existing_nodes = self.graph.nodes.all().count()
            self.identifier = number_of_existing_nodes
        super(AbstractNode, self).save(*args, **kwargs)

    def to_json(self, use_dict=False, **kwargs):
        """
            Representation of Node object in Json format
        """
        output = dict()
        output['id'] = self.identifier
        if self.label:
            output['label'] = self.label

        if use_dict:
            return output

        return json.dumps(output, cls=JSONEncoder, **kwargs)
