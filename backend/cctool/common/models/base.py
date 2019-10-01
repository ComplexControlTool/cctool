import uuid
from django.db.models import Model, UUIDField, DateTimeField


class TimeStampedModel(Model):
    # id = UUIDField(
    #     primary_key=True,
    #     default=uuid.uuid4,
    #     editable=False
    # )
    
    created_at = DateTimeField(
        auto_now_add=True,
        verbose_name='Created datetime stamp'
    )
    
    updated_at = DateTimeField(
        auto_now=True,
        verbose_name='Last updated datetime stamp'
    )

    class Meta:
        abstract = True

    @property
    def is_new(self):
        return (self.updated_at - self.created_at).total_seconds() < 0.001

    @property
    def is_modified(self):
        return (self.updated_at - self.created_at).total_seconds() >= 0.001