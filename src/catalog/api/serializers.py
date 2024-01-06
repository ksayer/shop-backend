from rest_framework import serializers

from catalog.models import Model


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['slug', 'image']
