# Generated by Django 4.2 on 2024-01-07 14:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0006_modelcard_arrow_projectcard_arrow_publication_arrow"),
    ]

    operations = [
        migrations.AddField(
            model_name="banner",
            name="address",
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name="banner",
            name="email",
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name="banner",
            name="phone",
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
