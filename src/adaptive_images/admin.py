from django.contrib import admin

from adaptive_images.models import AdaptiveImage, AdaptiveImageSetting, ImagePreset


@admin.register(AdaptiveImage)
class AdaptiveImageAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_compressed']
    search_fields = ['original__original_filename']


@admin.register(AdaptiveImageSetting)
class AdaptiveImageSettingAdmin(admin.ModelAdmin):
    list_display = ['name', 'desktop', 'mobile', 'is_image_compress']


@admin.register(ImagePreset)
class ImagePresetAdmin(admin.ModelAdmin):
    list_display = [
        'internal_name',
        '__str__',
        'type',
        'max_width',
        'max_height',
        'quality',
    ]
