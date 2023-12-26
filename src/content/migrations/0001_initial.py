# Generated by Django 4.2 on 2023-12-26 20:29

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("adaptive_images", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Banner",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("ordering", models.IntegerField(default=0)),
                ("pre_title", models.CharField(blank=True, max_length=256)),
                ("title", models.CharField(blank=True, max_length=256)),
                ("subtitle", models.CharField(blank=True, max_length=256)),
                ("description", models.TextField(blank=True)),
                (
                    "image_position",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("left", "Left"),
                            ("right", "Right"),
                            ("top", "Top"),
                            ("bottom", "Bottom"),
                        ],
                        max_length=32,
                    ),
                ),
            ],
            options={
                "db_table": "banner",
                "ordering": ["ordering", "-updated"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Page",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("ordering", models.IntegerField(default=0)),
                ("inner_title", models.CharField(max_length=64)),
                ("title", models.CharField(blank=True, max_length=64)),
                ("slug", models.SlugField()),
            ],
            options={
                "db_table": "page",
                "ordering": ["ordering", "-updated"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ContentBlock",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("ordering", models.IntegerField(default=0)),
                ("inner_title", models.CharField(max_length=128)),
                ("title", models.CharField(blank=True, max_length=128)),
                (
                    "page",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blocks",
                        to="content.page",
                    ),
                ),
            ],
            options={
                "db_table": "content_block",
                "ordering": ["ordering", "-updated"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Button",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("ordering", models.IntegerField(default=0)),
                ("text", models.CharField(max_length=64)),
                ("link", models.URLField()),
                (
                    "banner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="content.banner"
                    ),
                ),
            ],
            options={
                "db_table": "button",
                "ordering": ["ordering", "-updated"],
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="banner",
            name="block",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="banners",
                to="content.contentblock",
            ),
        ),
        migrations.AddField(
            model_name="banner",
            name="image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="adaptive_images.adaptiveimage",
            ),
        ),
    ]
