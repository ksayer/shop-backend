from django.db import models as d_models
from filer.fields.image import FilerImageField

from admintools.models import ActiveCoreModel, CoreModel
from catalog.models import Model


class Category(ActiveCoreModel):
    title = d_models.CharField(max_length=64)

    def __str__(self):
        return self.title


class Project(ActiveCoreModel):
    title = d_models.CharField(max_length=64)
    category = d_models.ForeignKey(Category, on_delete=d_models.CASCADE, related_name='projects')
    slug = d_models.SlugField(max_length=64, unique=True)
    models = d_models.ManyToManyField(Model, related_name='projects')
    architect = d_models.CharField(max_length=64)
    architect_url = d_models.URLField(max_length=255, blank=True)
    location = d_models.CharField(max_length=128)
    installer = d_models.CharField(max_length=128)
    installer_url = d_models.URLField(max_length=255, blank=True)
    description = d_models.TextField(blank=True)

    def __str__(self):
        return self.title


class ProjectImage(CoreModel):
    project = d_models.ForeignKey(Project, on_delete=d_models.CASCADE, related_name='images')
    image = FilerImageField(
        on_delete=d_models.CASCADE,
        related_name='project_images',
    )
    main = d_models.BooleanField(default=False)

    class Meta:
        constraints = [
            d_models.UniqueConstraint(
                fields=['project', 'main'],
                condition=d_models.Q(main=True),
                name='unique_main_per_project',
            )
        ]


class Feedback(CoreModel):
    name = d_models.CharField(max_length=64)
    text = d_models.TextField()
    avatar = FilerImageField(
        on_delete=d_models.CASCADE,
        related_name='avatars',
    )
    project = d_models.ForeignKey(
        Project,
        on_delete=d_models.CASCADE,
        related_name='feedbacks',
    )

    def __str__(self):
        return self.name
