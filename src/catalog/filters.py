from django.contrib import admin


def dropdown_filter_with_custom_title(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            instance.template = 'django_admin_listfilter_dropdown/dropdown_filter.html'
            return instance

    return Wrapper
