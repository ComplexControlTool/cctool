from django.db.models import CharField
from cctool.common.models import TimeStampedModel


class AbstractAnalysis(TimeStampedModel):
    CONTROL_NODES_ANALYSIS = 'CN'
    RBS_XCS_ANALYSIS = 'XCS'
    ANALYSIS_SET = (
        (CONTROL_NODES_ANALYSIS, 'Control nodes'),
        (RBS_XCS_ANALYSIS, 'RBS XCS'),
    )

    analysis_type = CharField(
        choices=ANALYSIS_SET,
        blank=False,
        default=CONTROL_NODES_ANALYSIS,
        max_length=3,
        verbose_name='type of analysis'
    )

    class Meta:
        abstract = True
        verbose_name = 'analysis'
        verbose_name_plural = 'analyses'

    def __str__(self):
        return self.analysis_type
