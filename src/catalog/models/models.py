from django.db import models
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField

from admintools.models import ActiveCoreModel, CoreModel
from catalog.models.managers import GroupQuerySet, ModelQuerySet, CategoryQuerySet


class Group(ActiveCoreModel):
    title = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    objects = GroupQuerySet.as_manager()

    def __str__(self):
        return self.title


class Category(ActiveCoreModel):
    objects = CategoryQuerySet.as_manager()
    title = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return f'{self.title} ({self.group})'


class Model(ActiveCoreModel):
    objects = ModelQuerySet.as_manager()

    title = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='models')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Modification(CoreModel):
    title = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    model = models.ForeignKey(Model, related_name='modifications', on_delete=models.CASCADE)

    class Meta(ActiveCoreModel.Meta):
        unique_together = ('model', 'slug')

    def __str__(self):
        return self.title


class Product(ActiveCoreModel):
    title = models.CharField('Product title (without model)', max_length=64, blank=True)
    slug = models.SlugField()
    modification = models.ForeignKey(
        'Modification',
        related_name='products',
        on_delete=models.CASCADE
    )
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
    scheme = FilerFileField(
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='products_with_schema',
    )

    class Meta(ActiveCoreModel.Meta):
        unique_together = ('modification', 'slug')

    def __str__(self):
        return f'{self.id}: {self.title}'


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


class AttributeGroup(CoreModel):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title


class AttributeBase(CoreModel):
    title = models.CharField(max_length=32)
    group = models.ForeignKey(AttributeGroup, related_name='%(class)ss', on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.title} ({self.group})'


class ColorAttributeBase(AttributeBase):
    color = models.CharField(max_length=32)

    class Meta:
        abstract = True


class Power(AttributeBase):
    ...


class Beam(AttributeBase):
    ...


class ColorIndex(AttributeBase):
    ...


class ColorTemperature(AttributeBase):
    ...


class BodyColor(ColorAttributeBase):
    ...


class FrameColor(ColorAttributeBase):
    ...


class CoverColor(ColorAttributeBase):
    ...


class Dimming(AttributeBase):
    ...


class BeamAngle(AttributeBase):
    ...


class Protection(AttributeBase):
    ...


class Size(AttributeBase):
    ...


class Property(CoreModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    power = models.ForeignKey(
        'Power',
        related_name='products',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    size = models.ForeignKey(
        'Size',
        related_name='properties',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    beam = models.ForeignKey(
        'Beam',
        related_name='properties',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    beam_angle = models.ForeignKey(
        'BeamAngle',
        related_name='properties',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    color_index = models.ForeignKey(
        'ColorIndex',
        related_name='properties',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    color_temperature = models.ForeignKey(
        'ColorTemperature',
        related_name='properties',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    body_color = models.ForeignKey(
        'BodyColor',
        related_name='properties',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    frame_color = models.ForeignKey(
        'FrameColor',
        related_name='properties',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    cover_color = models.ForeignKey(
        'CoverColor',
        related_name='properties',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    dimming = models.ForeignKey(
        'Dimming',
        related_name='properties',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    protection = models.ForeignKey(
        'Protection',
        related_name='properties',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
