from django.db import models

from adaptive_images.models import AdaptiveImage
from admintools.models import CoreModel
from catalog.models import Model


class Page(CoreModel):
    inner_title = models.CharField(max_length=64)
    title = models.CharField(max_length=64, blank=True)
    slug = models.SlugField()

    def __str__(self):
        return self.inner_title


class ContentBlock(CoreModel):
    page = models.ForeignKey(Page, related_name='blocks', on_delete=models.CASCADE)
    inner_title = models.CharField(max_length=128)
    title = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.title


class Banner(CoreModel):
    class ImagePosition(models.TextChoices):
        LEFT = 'left'
        RIGHT = 'right'
        TOP = 'top'
        BOTTOM = 'bottom'

    block = models.ForeignKey(ContentBlock, related_name='banners', on_delete=models.CASCADE)
    pre_title = models.CharField(max_length=256, blank=True)
    title = models.CharField(max_length=256, blank=True)
    subtitle = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)

    image = models.ForeignKey(
        AdaptiveImage,
        on_delete=models.PROTECT,
        related_name='banners',
    )
    image_position = models.CharField(max_length=32, choices=ImagePosition.choices, blank=True)

    def __str__(self):
        return f'{self.block} - {self.title}'


class Button(CoreModel):
    text = models.CharField(max_length=64)
    link = models.URLField()
    banner = models.ForeignKey(Banner, related_name='buttons', on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class ModelCard(CoreModel):
    image = models.ForeignKey(
        AdaptiveImage,
        on_delete=models.PROTECT,
        related_name='model_cards',
    )
    title = models.CharField(max_length=64)
    text = models.TextField()
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='model_cards')

    def __str__(self):
        return self.title
