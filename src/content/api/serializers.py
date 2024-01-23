from django.conf import settings
from rest_framework import serializers

from admintools.api.serializers import ImageSerializer
from content.models import (
    Banner,
    Button,
    ContentBlock,
    FeedbackCard,
    ModelCard,
    ProjectCard,
    Publication,
    Tab,
)


class ButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Button
        fields = [
            'id',
            'title',
            'link',
        ]


class TabSerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = Tab
        fields = [
            'id',
            'title',
            'description',
            'image',
        ]


class BannerSerializer(serializers.ModelSerializer):
    buttons = ButtonSerializer(many=True)
    tabs = TabSerializer(many=True)
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
            'tabs',
            'mobile_image',
            'phone',
            'address',
            'email',
            'type',
            'image',
        ]


class ModelCardSerializer(serializers.ModelSerializer):
    image = ImageSerializer(source='model.image')
    slug = serializers.CharField(source='model.slug')

    class Meta:
        model = ModelCard
        fields = ['id', 'slug', 'arrow', 'type', 'title', 'description', 'image']


class ProjectCardSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    slug = serializers.CharField(source='project.slug')

    class Meta:
        model = ProjectCard
        fields = ['id', 'slug', 'arrow', 'type', 'title', 'description', 'image']

    def get_image(self, instance):
        return {
            'id': instance.main_image_id,
            'width': instance.main_image_width,
            'height': instance.main_image_height,
            'optimized': instance.main_image_optimized,
            'absolute_url': f'{settings.HOST_DOMAIN}/media/{instance.main_image_path}',
        }


class FeedbackCardSerializer(serializers.ModelSerializer):
    image = ImageSerializer(source='feedback.avatar')
    slug = serializers.CharField(source='feedback.project.slug')
    title = serializers.CharField(source='feedback.name')
    subtitle = serializers.CharField(source='feedback.project.title')
    description = serializers.CharField(source='feedback.description')

    class Meta:
        model = FeedbackCard
        fields = ['id', 'slug', 'type', 'title', 'subtitle', 'description', 'image']


class PublicationSerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = Publication
        fields = ['id', 'slug', 'arrow', 'type', 'title', 'image']


class ContentBlockSerializer(serializers.ModelSerializer):
    banners = serializers.SerializerMethodField()
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
            'type',
        ]

    def get_banners(self, instance):
        if instance.consultant:
            return BannerSerializer(instance=[instance.consultant[0]], many=True).data
        return BannerSerializer(instance=instance.banners, many=True).data

    def get_cards(self, instance):
        if instance.modelcards.exists():
            return ModelCardSerializer(instance=instance.modelcards, many=True).data
        if instance.projectcards.exists():
            return ProjectCardSerializer(instance=instance.projectcards, many=True).data
        if instance.feedbackcards.exists():
            return FeedbackCardSerializer(instance=instance.feedbackcards, many=True).data
        if instance.publications.exists():
            return PublicationSerializer(instance=instance.publications, many=True).data
        return []
