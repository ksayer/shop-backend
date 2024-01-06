from django.conf import settings
from django.contrib import admin
from filer.admin.imageadmin import ImageAdmin
from filer.utils.loader import load_model

Image = load_model(settings.FILER_IMAGE_MODEL)


class FilerImageAdmin(ImageAdmin):
    pass


FilerImageAdmin.fieldsets = FilerImageAdmin.build_fieldsets(
    extra_main_fields=('default_alt_text', 'default_caption', 'optimized'),
    extra_fieldsets=(
        (
            'Subject Location',
            {
                'fields': ('subject_location',),
                'classes': ('collapse',),
            },
        ),
    ),
)

# Unregister the default admin
admin.site.unregister(Image)
# Register your own
admin.site.register(Image, FilerImageAdmin)
