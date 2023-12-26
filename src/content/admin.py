from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline  # type: ignore

from content.models import Banner, Block, Button, Page


class ButtonInline(NestedStackedInline):
    model = Button
    extra = 0
    fk_name = 'banner'


class BannerInline(NestedStackedInline):
    model = Banner
    extra = 0
    inlines = (ButtonInline,)
    fk_name = 'block'


class BlockInline(NestedStackedInline):
    model = Block
    extra = 0
    inlines = (BannerInline,)
    fk_name = 'page'


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'block')
    list_filter = ('block',)
    inlines = (ButtonInline,)


@admin.register(Block)
class BlockAdmin(NestedModelAdmin):
    list_display = ('page', 'title')
    list_filter = ('page',)
    inlines = (BannerInline,)


@admin.register(Page)
class PageAdmin(NestedModelAdmin):
    list_display = ('title',)
    inlines = (BlockInline,)
