import json
from django.contrib.postgres.fields import JSONField
from django.db.models import CharField, OneToOneField, CASCADE, ForeignKey
from rest_framework.utils.encoders import JSONEncoder
from cctool.common.models import TimeStampedModel
from cctool.common.enums import AnalysisOption, AnalysisShortcode


class AbstractAnalysis(TimeStampedModel):
    analysis_type = CharField(
        choices=list(zip(AnalysisShortcode.__values__, AnalysisOption.__values__)),
        blank=False,
        default=AnalysisShortcode.CONTROLLABILITY_ANALYSIS.value,
        max_length=3,
        verbose_name='type of analysis'
    )

    data = JSONField(
        default=dict,
        null=True,
        blank=True
    )

    visualization = OneToOneField(
        'graphs.Visualization',
        on_delete=CASCADE,
        primary_key=False
    )

    graph = ForeignKey(
        'graphs.Graph',
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name='analyses',
        related_query_name='analysis'
    )

    node = ForeignKey(
        'graphs.Node',
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name='analyses',
        related_query_name='analysis'
    )

    edge = ForeignKey(
        'graphs.Edge',
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name='analyses',
        related_query_name='analysis'
    )

    class Meta:
        abstract = True
        verbose_name = 'analysis'
        verbose_name_plural = 'analyses'

    def __str__(self):
        return self.get_analysis_type_display()

    def to_json(self, use_dict=False, **kwargs):
        """
            Representation of Analysis object in Json format
        """
        analysis = dict()
        analysis['typeOfAnalysis'] = self.get_analysis_type_display()
        analysis['data'] = self.data
        
        output = dict()
        output['analysis'] = analysis
        output['visualization'] = self.visualization.to_json(use_dict=True, **kwargs)

        if use_dict:
            return output

        return json.dumps(output, cls=JSONEncoder, **kwargs)
