import json
from django.contrib.postgres.fields import JSONField
from rest_framework.utils.encoders import JSONEncoder
from cctool.common.models import TimeStampedModel


class AbstractStructure(TimeStampedModel):
    data = JSONField(
      default=dict,
      null=True,
      blank=True
    )

    class Meta:
        abstract = True
        verbose_name = 'structure'
        verbose_name_plural = 'structures'

    def to_json(self, use_dict=False, **kwargs):
        """
            Representation of Structure object in Json format
        """
        output = self.data

        if use_dict:
            return output

        return json.dumps(output, cls=JSONEncoder, **kwargs)