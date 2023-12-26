from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline  # type: ignore

from content.models import Banner, Button, ContentBlock, Page


class ButtonInline(NestedStackedInline):
    model = Button
    extra = 0
    fk_name = 'banner'


class BannerInline(NestedStackedInline):
    model = Banner
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
    list_display = ('title', 'block')
    list_filter = ('block',)
    inlines = (ButtonInline,)


@admin.register(ContentBlock)
class ContentBlockAdmin(NestedModelAdmin):
    list_display = ('inner_title', 'page', 'title')
    list_filter = ('page',)
    inlines = (BannerInline,)


@admin.register(Page)
class PageAdmin(NestedModelAdmin):
    list_display = (
        'inner_title',
        'title',
    )
    inlines = (ContentBlockInline,)
