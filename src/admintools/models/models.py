import uuid

from django.db import models


class CoreModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    ordering = models.IntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['ordering', '-updated']
