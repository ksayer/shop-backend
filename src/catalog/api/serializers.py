from rest_framework import serializers

from admintools.utils import remove_duplicated_values
from catalog.models import Category, Group, Model


class ModelListSerializer(serializers.ModelSerializer):
    color_temperatures = serializers.JSONField()
    images = serializers.SerializerMethodField()
    min_price = serializers.DecimalField(max_digits=10, decimal_places=0)
    min_discounted_price = serializers.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        model = Model
        fields = [
            'id',
            'title',
            'slug',
            'min_price',
            'min_discounted_price',
            'color_temperatures',
            'images',
        ]

    def get_images(self, instance):
        """Remove color duplicates"""
        return remove_duplicated_values(instance.images, 'color')


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


class GroupListSerializer(serializers.ModelSerializer):
    categories = CategoryListSerializer(many=True)
    filters = serializers.JSONField()

    class Meta:
        model = Group
        fields = ['id', 'title', 'slug', 'filters', 'categories']
