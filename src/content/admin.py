from django.contrib import admin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from nested_inline.admin import NestedModelAdmin, NestedStackedInline  # type: ignore

from content.models import (
    Banner,
    Button,
    ContentBlock,
    FeedbackCard,
    ModelCard,
    Page,
    ProjectCard,
    Publication,
)


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
    list_display = ('id', 'title', 'block', 'ordering')
    list_editable = ['ordering']
    list_filter = (('block', RelatedDropdownFilter),)
    inlines = (ButtonInline,)


@admin.register(ContentBlock)
class ContentBlockAdmin(NestedModelAdmin):
    autocomplete_fields = ['page']
    list_display = ('id', 'inner_title', 'title', 'page', 'title', 'ordering')
    list_editable = ['ordering']
    list_filter = ('page',)
    inlines = (BannerInline,)
    search_fields = ['title', 'inner_title']


@admin.register(Page)
class PageAdmin(NestedModelAdmin):
    list_display = (
        'id',
        'inner_title',
        'title',
    )
    inlines = (ContentBlockInline,)
    search_fields = ['title', 'inner_title']


@admin.register(ModelCard)
class ModelCardAdmin(admin.ModelAdmin):
    autocomplete_fields = ['model', 'block']
    list_display = ('id', 'title', 'block', 'ordering')
    list_editable = ('ordering',)


@admin.register(ProjectCard)
class ProjectCardAdmin(admin.ModelAdmin):
    autocomplete_fields = ['project', 'block']
    list_display = ('id', 'title', 'block', 'ordering')
    list_editable = ('ordering',)


@admin.register(FeedbackCard)
class FeedbackCardAdmin(admin.ModelAdmin):
    autocomplete_fields = ['feedback', 'block']
    list_display = ('id', 'feedback', 'block', 'ordering')
    list_editable = ('ordering',)


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['block']
    list_display = ['id', 'title', 'block', 'ordering']
    list_editable = ['ordering']
    search_fields = ['title']
