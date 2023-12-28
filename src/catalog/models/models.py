from django.db import models
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField

from adaptive_images.models import AdaptiveImage
from admintools.models import CoreModel, ActiveCoreModel


class Group(ActiveCoreModel):
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title


class Category(ActiveCoreModel):
    title = models.CharField(max_length=64)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='groups')

    def __str__(self):
        return self.title


class Model(ActiveCoreModel):
    title = models.CharField(max_length=64)
    slug = models.SlugField(unique=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='models')
    description = models.TextField(blank=True)
    image = models.ForeignKey(
        AdaptiveImage,
        on_delete=models.PROTECT,
        related_name='models',
    )

    def __str__(self):
        return self.title


class Product(ActiveCoreModel):
    title = models.CharField('Product title (without model)', max_length=64, blank=True)
    slug = models.SlugField(unique=False)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    discounted_price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
    )
    image_opaque = FilerImageField(
        on_delete=models.SET_NULL,
        help_text='With an opaque background. (used by Yandex Direct)',
        related_name='products_with_image_opaque',
        blank=True,
        null=True,
    )
    image = models.ForeignKey(
        AdaptiveImage,
        on_delete=models.PROTECT,
        related_name='products',
    )
    schema = FilerFileField(
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='products_with_schema',
    )
    modification = models.ForeignKey('Modification', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}: {self.title}'

    def get_body_color(self, value: bool = True):
        if (body_color := self.properties.filter(title='body_color').first()) and value:
            return body_color.value
        return body_color


class Modification(CoreModel):
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title


class ProductFile(CoreModel):
    file = FilerFileField(on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='files',
    )

    def __str__(self):
        return self.name


class ProductProperty(CoreModel):
    """
    Intermediate model for products and properties. Explicitly created
    for admin interface.
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_properties'
    )
    property = models.ForeignKey(
        'Property', on_delete=models.CASCADE, related_name='product_properties'
    )

    def __str__(self):
        return self.property.get_title_display()


class Property(CoreModel):
    class Title(models.TextChoices):
        POWER = 'power'
        BEAM = 'beam'
        COLOR_INDEX = 'color_index'
        COLOR_TEMPERATURE = 'color_temperature'
        BODY_COLOR = 'body_color'
        FRAME_COLOR = 'frame_color'
        COVER_COLOR = 'cover_color'
        DIMMING = 'dimming'
        BEAM_ANGLE = 'beam_angle'
        PROTECTION = 'protection'
        SIZE = 'size'

    title = models.CharField(max_length=32, choices=Title.choices)
    value = models.CharField(max_length=32)
    color_code = models.CharField(max_length=32, blank=True)
    group = models.ForeignKey('PropertyGroup', on_delete=models.CASCADE, related_name='properties')
    products = models.ManyToManyField(Product, related_name='properties', through=ProductProperty)

    def __str__(self):
        return f'{self.get_title_display()}: {self.value}'


class PropertyGroup(CoreModel):
    title = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.title} ({self.property_title})'

    @property
    def property_title(self):
        if prop := self.properties.first():
            return prop.get_title_display()
