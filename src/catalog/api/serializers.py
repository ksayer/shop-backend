from rest_framework import serializers

from admintools.api.serializers import ImageSerializer
from admintools.utils import remove_duplicated_values
from catalog.models import (
    Banner,
    Beam,
    BeamAngle,
    BodyColor,
    Category,
    ColorIndex,
    ColorTemperature,
    CoverColor,
    Dimming,
    FrameColor,
    Gallery,
    Group,
    Model,
    Modification,
    Power,
    Product,
    Property,
    Protection,
    Size,
)
from catalog.utils import group_filters


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


class BannerSerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = Banner
        fields = [
            'id',
            'title',
            'description',
            'image',
        ]


class GallerySerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = Gallery
        fields = ['id', 'image']


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'id',
            'title',
        ]

    def __init__(self, *args, **kwargs):
        self.Meta.model = kwargs.pop('model')
        super().__init__(*args, **kwargs)


class ColoredAttributeSerializer(AttributeSerializer):
    class Meta(AttributeSerializer.Meta):
        fields = AttributeSerializer.Meta.fields + ['color']


class PropertySerializer(serializers.ModelSerializer):
    power = AttributeSerializer(model=Power)
    beam = AttributeSerializer(model=Beam)
    color_index = AttributeSerializer(model=ColorIndex)
    color_temperature = AttributeSerializer(model=ColorTemperature)
    dimming = AttributeSerializer(model=Dimming)
    beam_angle = AttributeSerializer(model=BeamAngle)
    protection = AttributeSerializer(model=Protection)
    size = AttributeSerializer(model=Size)
    body_color = ColoredAttributeSerializer(model=BodyColor)
    frame_color = ColoredAttributeSerializer(model=FrameColor)
    cover_color = ColoredAttributeSerializer(model=CoverColor)

    class Meta:
        model = Property
        fields = [
            'power',
            'beam',
            'color_index',
            'color_temperature',
            'body_color',
            'frame_color',
            'cover_color',
            'dimming',
            'beam_angle',
            'protection',
            'size',
        ]


class ProductSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    scheme = ImageSerializer()
    property = PropertySerializer()

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'slug',
            'price',
            'discounted_price',
            'image',
            'scheme',
            'property',
        ]


class ModificationSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Modification
        fields = ['id', 'title', 'slug', 'products']


class GroupLimitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']


class CategoryLimitedSerializer(serializers.ModelSerializer):
    group = GroupLimitedSerializer()

    class Meta:
        model = Category
        fields = ['id', 'slug', 'title', 'group']


class ModelRetrieveSerializer(serializers.ModelSerializer):
    min_price = serializers.DecimalField(max_digits=10, decimal_places=0)
    min_discounted_price = serializers.DecimalField(max_digits=10, decimal_places=0)
    banners = BannerSerializer(many=True)
    gallery = GallerySerializer(many=True)
    modifications = ModificationSerializer(many=True)
    category = CategoryLimitedSerializer()

    class Meta:
        model = Model
        fields = [
            'id',
            'title',
            'description',
            'slug',
            'min_price',
            'min_discounted_price',
            'category',
            'banners',
            'gallery',
            'modifications',
        ]


class CategoryListSerializer(serializers.ModelSerializer):
    filters = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'filters']

    def get_filters(self, instance):
        return group_filters(instance.filters)


class GroupListSerializer(serializers.ModelSerializer):
    categories = CategoryListSerializer(many=True)
    filters = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'title', 'slug', 'filters', 'categories']

    def get_filters(self, instance):
        return group_filters(instance.filters)
