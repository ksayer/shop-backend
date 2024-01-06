from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline  # type: ignore

from content.models import Banner, Button, ContentBlock, Page, ModelCard


class ButtonInline(NestedStackedInline):
    model = Button
    extra = 0
    fk_name = 'banner'


class BannerInline(NestedStackedInline):
    model = Banner
    autocomplete_fields = ['image']
    extra = 0
    inlines = (ButtonInline,)
    fk_name = 'block'


class ContentBlockInline(NestedStackedInline):
    model = ContentBlock
    extra = 0
    inlines = (BannerInline,)
    fk_name = 'page'


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    autocomplete_fields = ['block', 'image']
    list_display = ('title', 'block', 'ordering')
    list_filter = ('block',)
    inlines = (ButtonInline,)


@admin.register(ContentBlock)
class ContentBlockAdmin(NestedModelAdmin):
    autocomplete_fields = ['page']
    list_display = ('inner_title', 'title', 'page', 'title')
    list_filter = ('page',)
    inlines = (BannerInline,)
    search_fields = ['title', 'inner_title']


@admin.register(Page)
class PageAdmin(NestedModelAdmin):
    list_display = (
        'inner_title',
        'title',
    )
    inlines = (ContentBlockInline,)
    search_fields = ['title', 'inner_title']


@admin.register(ModelCard)
class ModelCardAdmin(admin.ModelAdmin):
    autocomplete_fields = ['model', 'image']
    list_display = ('title', 'ordering')
    list_editable = ('ordering', )
    model = ModelCard
