import uuid

from django.conf import settings
from django.db import models
from filer.models import BaseImage


class CoreModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    ordering = models.IntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['ordering', '-updated']


class ActiveCoreModel(CoreModel):
    active = models.BooleanField(default=True)

    class Meta(CoreModel.Meta):
        abstract = True


class FilerImage(BaseImage):
    optimized = models.BooleanField(default=False)

    class Meta(BaseImage.Meta):
        app_label = 'admintools'
        default_manager_name = 'objects'

    @property
    def absolute_url(self):
        return f'{settings.HOST_DOMAIN}{self.url}'
