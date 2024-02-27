from django.contrib import admin

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
    ProductFile,
    Property,
    Protection,
    Size,
)


class ProductFileInline(admin.TabularInline):
    extra = 1
    model = ProductFile


class BannerInline(admin.TabularInline):
    model = Banner
    extra = 1


class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'ordering']
    list_editable = ['ordering', 'active']
    search_fields = ['title']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    autocomplete_fields = ['group']
    list_display = ['title', 'active', 'ordering']
    list_editable = ['ordering', 'active']
    search_fields = ['title']


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    list_display = ['title', 'active', 'slug', 'ordering']
    list_editable = ['ordering', 'active']
    inlines = [BannerInline, GalleryInline]
    search_fields = ['title']


@admin.register(Modification)
class ModificationAdmin(admin.ModelAdmin):
    search_fields = ['title']


class PropertyInline(admin.StackedInline):
    autocomplete_fields = [
        'power',
        'size',
        'beam',
        'beam_angle',
        'color_index',
        'color_temperature',
        'body_color',
        'frame_color',
        'cover_color',
        'dimming',
        'protection',
    ]
    model = Property
    fieldsets = [
        (
            '',
            {
                'fields': [
                    (
                        'body_color',
                        'color_temperature',
                    ),
                    ('power', 'beam'),
                    ('beam_angle', 'color_index'),
                    ('frame_color', 'cover_color'),
                    ('dimming', 'protection'),
                    ('size',),
                ],
            },
        ),
    ]
    can_delete = False
    template = 'admintools/stacked_inline_o2o.html'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (PropertyInline, ProductFileInline)
    autocomplete_fields = ['image', 'modification']
    list_display = [
        'id',
        'modification',
        'slug',
        'active',
        'price',
        'discounted_price',
        'ordering',
    ]
    list_editable = ['price', 'discounted_price', 'active', 'ordering']
    search_fields = ['slug', 'title', 'modification__title', 'modification__model__title']
    search_help_text = 'searching by slug, title'


class PropertyAdmin(admin.ModelAdmin):
    search_fields = ['title', 'group']


properties = [
    Power,
    Beam,
    ColorIndex,
    ColorTemperature,
    BodyColor,
    FrameColor,
    CoverColor,
    Dimming,
    BeamAngle,
    Protection,
    Size,
]


def register_properties(models):
    for model in models:
        admin.register(model)(PropertyAdmin)


register_properties(properties)
