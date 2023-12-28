from django.contrib import admin

from projects.forms import ProjectImageInlineFormset
from projects.models import Project, ProjectImage, Category


class ProjectImageInline(admin.TabularInline):
    autocomplete_fields = ['image']
    model = ProjectImage
    formset = ProjectImageInlineFormset


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    list_display = ['title', 'category', 'architect', 'location', 'installer']
    list_filter = ['category']
    inlines = [ProjectImageInline]
    search_fields = ['title', 'architect', 'location', 'installer']

