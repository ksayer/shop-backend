from rest_framework import serializers

from content.models import Banner, Button, ContentBlock


class ButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Button
        fields = [
            'text',
            'link',
        ]


class BannerSerializer(serializers.ModelSerializer):
    buttons = ButtonSerializer(many=True)

    class Meta:
        model = Banner
        fields = [
            'pre_title',
            'title',
            'subtitle',
            'description',
            'image_position',
            'image',
            'buttons',
        ]


class ContentBlockSerializer(serializers.ModelSerializer):
    banners = BannerSerializer(many=True)

    class Meta:
        model = ContentBlock
        fields = [
            'title',
            'banners',
        ]
