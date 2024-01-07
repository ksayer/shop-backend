from django.conf import settings
from rest_framework import serializers

from admintools.api.serializers import ImageSerializer
from content.models import Banner, Button, ContentBlock, ModelCard, ProjectCard


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
            'mobile_image',
            'image',
        ]


class ModelCardSerializer(serializers.ModelSerializer):
    image = ImageSerializer(source='model.image')
    slug = serializers.CharField(source='model.slug')

    class Meta:
        model = ModelCard
        fields = ['id', 'slug', 'type', 'title', 'text', 'image']


class ProjectCardSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    slug = serializers.CharField(source='project.slug')

    class Meta:
        model = ProjectCard
        fields = ['id', 'slug', 'type', 'title', 'text', 'image']

    def get_image(self, instance):
        return {
            'id': instance.main_image_id,
            'width': instance.main_image_width,
            'height': instance.main_image_height,
            'optimized': instance.main_image_optimized,
            'absolute_url': f'{settings.HOST_DOMAIN}/media/{instance.main_image_path}',
        }


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
            'form',
        ]

    def get_cards(self, instance):
        if instance.modelcards.exists():
            return ModelCardSerializer(instance=instance.modelcards, many=True).data
        if instance.projectcards.exists():
            return ProjectCardSerializer(instance=instance.projectcards, many=True).data
        return []
