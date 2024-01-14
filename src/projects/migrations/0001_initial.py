# Generated by Django 4.2 on 2024-01-14 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("ordering", models.IntegerField(default=0)),
                ("active", models.BooleanField(default=True)),
                ("title", models.CharField(max_length=64)),
            ],
            options={
                "ordering": ["ordering", "-updated"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("ordering", models.IntegerField(default=0)),
                ("active", models.BooleanField(default=True)),
                ("title", models.CharField(max_length=64)),
                ("slug", models.SlugField(max_length=64, unique=True)),
                ("architect", models.CharField(max_length=64)),
                ("architect_url", models.URLField(blank=True, max_length=255)),
                ("location", models.CharField(max_length=128)),
                ("installer", models.CharField(max_length=128)),
                ("installer_url", models.URLField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="projects",
                        to="projects.category",
                    ),
                ),
                ("models", models.ManyToManyField(related_name="projects", to="catalog.model")),
            ],
            options={
                "ordering": ["ordering", "-updated"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProjectImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("ordering", models.IntegerField(default=0)),
                ("main", models.BooleanField(default=False)),
                (
                    "image",
                    filer.fields.image.FilerImageField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="project_images",
                        to=settings.FILER_IMAGE_MODEL,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="projects.project",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Feedback",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("ordering", models.IntegerField(default=0)),
                ("name", models.CharField(max_length=64)),
                ("description", models.TextField()),
                (
                    "avatar",
                    filer.fields.image.FilerImageField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="avatars",
                        to=settings.FILER_IMAGE_MODEL,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feedbacks",
                        to="projects.project",
                    ),
                ),
            ],
            options={
                "ordering": ["ordering", "-updated"],
                "abstract": False,
            },
        ),
        migrations.AddConstraint(
            model_name="projectimage",
            constraint=models.UniqueConstraint(
                condition=models.Q(("main", True)),
                fields=("project", "main"),
                name="unique_main_per_project",
            ),
        ),
    ]
