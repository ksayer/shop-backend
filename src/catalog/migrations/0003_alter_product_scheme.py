# Generated by Django 4.2 on 2024-02-26 20:02

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ("catalog", "0002_alter_product_modification_alter_property_beam_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="scheme",
            field=filer.fields.image.FilerImageField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="products_with_schema",
                to=settings.FILER_IMAGE_MODEL,
            ),
        ),
    ]
