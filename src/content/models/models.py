from django.db import models
from filer.fields.image import FilerImageField

from admintools.models import CoreModel
from catalog.models import Model
from content.models.managers import ProjectCardQuerySet
from projects.models import Project, Feedback


class Page(CoreModel):
    inner_title = models.CharField(max_length=64)
    title = models.CharField(max_length=64, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.inner_title


class ContentBlock(CoreModel):
    class Type(models.TextChoices):
        CONSULT_FORM = 'CONSULT_FORM', 'Get consultation form'
        CATALOG_FORM = 'CATALOG_FORM', 'Get catalog form'
        BANNERS = 'BANNERS', 'Simple banners'
        WIDE_BANNERS = 'WIDE_BANNERS', 'Wide banners'

    page = models.ForeignKey(Page, related_name='blocks', on_delete=models.CASCADE)
    inner_title = models.CharField(max_length=128)
    title = models.CharField(max_length=128, blank=True)
    link = models.CharField(max_length=128, blank=True)
    link_text = models.CharField(max_length=128, blank=True)
    type = models.CharField(choices=Type.choices, default=Type.BANNERS)

    def __str__(self):
        return self.inner_title


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
    mobile_image = models.BooleanField(
        help_text='Show image on mobile devices (screens < 1024px)', default=True
    )
    image = FilerImageField(
        on_delete=models.CASCADE,
        related_name='banners',
    )
    image_position = models.CharField(max_length=32, choices=ImagePosition.choices, blank=True)

    phone = models.CharField(max_length=256, blank=True)
    address = models.CharField(max_length=256, blank=True)
    email = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f'{self.block} - {self.title}'


class Button(CoreModel):
    text = models.CharField(max_length=64)
    link = models.CharField(max_length=128, blank=True)
    banner = models.ForeignKey(Banner, related_name='buttons', on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class CardBase(CoreModel):
    block = models.ForeignKey(ContentBlock, related_name='%(class)ss', on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    arrow = models.BooleanField(default=False)
    text = models.TextField()

    class Meta(CoreModel.Meta):
        abstract = True

    def __str__(self):
        return self.title


class ModelCard(CardBase):
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='modelcards')

    @property
    def type(self):
        return 'model'


class ProjectCard(CardBase):
    objects = ProjectCardQuerySet.as_manager()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projectcards')

    @property
    def type(self):
        return 'project'


class FeedbackCard(CoreModel):
    block = models.ForeignKey(ContentBlock, related_name='%(class)ss', on_delete=models.CASCADE)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='feedbackcards')

    @property
    def type(self):
        return 'feedback'


class Publication(CardBase):
    block = models.ForeignKey(ContentBlock, related_name='%(class)ss', on_delete=models.CASCADE)
    image = FilerImageField(
        on_delete=models.CASCADE,
        related_name='pubcitationcards',
    )
    slug = models.SlugField(unique=True)

    @property
    def type(self):
        return 'publication'
