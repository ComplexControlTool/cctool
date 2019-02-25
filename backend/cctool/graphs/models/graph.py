import json
from collections import OrderedDict
from django.db.models import ForeignKey, OneToOneField, CharField, TextField, CASCADE
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

    structure = OneToOneField(
        'graphs.Structure',
        on_delete=CASCADE,
        primary_key=False
    )

    visualization = OneToOneField(
        'graphs.Visualization',
        on_delete=CASCADE,
        primary_key=False
    )

    class Meta:
        abstract = True
        verbose_name = 'graph'
        verbose_name_plural = 'graphs'

    def __str__(self):
        return self.title

    def to_json(self, use_dict=False, **kwargs):
        """
            Representation of Graph object in Json format
        """
        output = dict()
        output['title'] = self.title
        output['description'] = self.description
        output['structure'] = self.structure.to_json(use_dict=True, **kwargs)
        output['visualization'] = self.visualization.to_json(use_dict=True, **kwargs)

        if use_dict:
            return output

        return json.dumps(output, cls=JSONEncoder, **kwargs)
