from rest_framework import serializers

from admintools.models import FilerImage


class ImageSerializer(serializers.ModelSerializer):
    width = serializers.IntegerField(source='_width')
    height = serializers.IntegerField(source='_height')

    class Meta:
        model = FilerImage
        fields = ['id', 'absolute_url', 'width', 'height', 'optimized']
