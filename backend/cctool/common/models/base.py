from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @property
    def is_new(self):
        return (self.updated_at - self.created_at).total_seconds() < 0.001

    @property
    def is_modified(self):
        return (self.updated_at - self.created_at).total_seconds() >= 0.001