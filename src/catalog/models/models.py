from django.db import models
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField

from admintools.models import ActiveCoreModel, CoreModel
from catalog.models.managers import ModelQuerySet, PropertyQuerySet


class Group(ActiveCoreModel):
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title


class Category(ActiveCoreModel):
    title = models.CharField(max_length=64)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='groups')

    def __str__(self):
        return f'{self.title} ({self.group})'


class Model(ActiveCoreModel):
    objects = ModelQuerySet.as_manager()

    title = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='models')
    description = models.TextField(blank=True)
    image = FilerImageField(
        on_delete=models.CASCADE,
        related_name='models',
    )

    def __str__(self):
        return self.title


class Product(ActiveCoreModel):
    title = models.CharField('Product title (without model)', max_length=64, blank=True)
    slug = models.SlugField(unique=False)
    model = models.ForeignKey(Model, related_name='products', on_delete=models.CASCADE)
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
    image = FilerImageField(
        on_delete=models.CASCADE,
        related_name='products',
    )
    schema = FilerFileField(
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='products_with_schema',
    )
    modification = models.ForeignKey('Modification', on_delete=models.CASCADE)

    class Meta(ActiveCoreModel.Meta):
        unique_together = ('model', 'slug')

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
    objects = PropertyQuerySet.as_manager()

    class Title(models.TextChoices):
        POWER = 'power', 'Мощность'
        BEAM = 'beam', 'Световой поток'
        COLOR_INDEX = 'color_index', 'Индекс цветопередачи'
        COLOR_TEMPERATURE = 'color_temperature', 'Цветовая температура'
        BODY_COLOR = 'body_color', 'Цвет корпуса'
        FRAME_COLOR = 'frame_color', 'Цвет рамки'
        COVER_COLOR = 'cover_color', 'Цвет накладки'
        DIMMING = 'dimming', 'Управление яркостью'
        BEAM_ANGLE = 'beam_angle', 'Угол рассеивания'
        PROTECTION = 'protection', 'Влагозащита'
        SIZE = 'size', 'Размер'

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
