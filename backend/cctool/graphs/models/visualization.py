import json
from django.contrib.postgres.fields import JSONField
from rest_framework.utils.encoders import JSONEncoder
from cctool.common.models import TimeStampedModel


class AbstractVisualization(TimeStampedModel):
    options = JSONField(
      default=dict,
      null=True,
      blank=True
    )

    structure = JSONField(
      default=dict,
      null=True,
      blank=True
    )

    class Meta:
        abstract = True
        verbose_name = 'visualization'
        verbose_name_plural = 'visualizations'

    def to_json(self, use_dict=False, **kwargs):
        """
            Representation of Visualization object in Json format
        """
        output = dict()
        output['options'] = self.options
        output['structure'] = self.structure

        if use_dict:
            return output

        return json.dumps(output, cls=JSONEncoder, **kwargs)