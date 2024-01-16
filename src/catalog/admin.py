from django.contrib import admin
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter,
    RelatedDropdownFilter,
)

from catalog.filters import dropdown_filter_with_custom_title
from catalog.forms import ProductPropertyInlineFormset, PropertyForm
from catalog.models import (
    Category,
    Group,
    Model,
    Modification,
    Product,
    ProductFile,
    ProductProperty,
    Property,
    PropertyGroup,
)


class ProductPropertyInline(admin.TabularInline):
    autocomplete_fields = ['property']
    formset = ProductPropertyInlineFormset
    model = ProductProperty


class ProductFileInline(admin.TabularInline):
    extra = 1
    model = ProductFile


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
    autocomplete_fields = ['category', 'image']
    list_display = ['title', 'active', 'slug', 'ordering']
    list_editable = ['ordering', 'active']
    search_fields = ['title']


@admin.register(Modification)
class ModificationAdmin(admin.ModelAdmin):
    search_fields = ['title']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['image', 'modification', 'model']
    list_display = ['id', 'slug', 'title', 'model', 'active', 'price', 'discounted_price','body_color', 'ordering']
    list_editable = ['price', 'discounted_price', 'active', 'ordering']
    inlines = [ProductPropertyInline, ProductFileInline]
    search_fields = ['slug', 'title', 'model__title']
    search_help_text = 'searching by slug, title'

    def body_color(self, instance):
        return instance.get_body_color()


@admin.register(PropertyGroup)
class PropertyGroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'property', 'ordering']
    list_editable = ['ordering']
    list_filter = [('properties__title', dropdown_filter_with_custom_title('property'))]
    search_fields = ['title']

    def property(self, obj):
        return obj.property_title


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    autocomplete_fields = ['group']
    exclude = ['ordering']
    form = PropertyForm
    list_display = ['title', 'value', 'color_code', 'group']
    list_editable = ['group']
    list_filter = [('group', RelatedDropdownFilter), ('title', DropdownFilter)]
    search_fields = ['display_title', 'value']
    search_help_text = 'searching by title, value'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.with_display_title()
