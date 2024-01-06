from rest_framework import serializers

from admintools.api.serializers import ImageSerializer
from content.models import Banner, Button, ContentBlock, ModelCard


class ButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Button
        fields = [
            'id',
            'text',
            'link',
        ]


class BannerSerializer(serializers.ModelSerializer):
    buttons = ButtonSerializer(many=True)
    image = ImageSerializer()

    class Meta:
        model = Banner
        fields = [
            'id',
            'pre_title',
            'title',
            'subtitle',
            'description',
            'image_position',
            'buttons',
            'image',
        ]


class ModelCardSerializer(serializers.ModelSerializer):
    image = ImageSerializer(source='model.image')
    slug = serializers.CharField(source='model.slug')

    class Meta:
        model = ModelCard
        fields = ['id', 'slug', 'type', 'title', 'text', 'image']


class ContentBlockSerializer(serializers.ModelSerializer):
    banners = BannerSerializer(many=True)
    cards = serializers.SerializerMethodField()

    class Meta:
        model = ContentBlock
        fields = [
            'id',
            'ordering',
            'title',
            'link',
            'link_text',
            'cards',
            'banners',
        ]

    def get_cards(self, instance):
        if instance.model_cards.exists():
            return ModelCardSerializer(instance=instance.model_cards, many=True).data
        return []
