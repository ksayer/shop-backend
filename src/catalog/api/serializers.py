from django.conf import settings
from rest_framework import serializers

from catalog.models import Model


class ModelListSerializer(serializers.ModelSerializer):
    color_temperatures = serializers.JSONField()
    images = serializers.SerializerMethodField()
    min_price = serializers.DecimalField(max_digits=10, decimal_places=0)
    min_discounted_price = serializers.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        model = Model
        fields = [
            'title',
            'slug',
            'min_price',
            'min_discounted_price',
            'color_temperatures',
            'images',
        ]

    def get_images(self, instance):
        return [
            {
                'color': color,
                'image': f'{settings.HOST_DOMAIN}/media/{instance.images[i]}'
            }
            for i, color in enumerate(instance.colors)
        ]

