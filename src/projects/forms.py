from django import forms
from django.core.exceptions import ValidationError


class ProjectImageInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        """Check that project has 1 main image"""
        if self.is_valid():
            main_values = [prop.get('main', False) for prop in self.cleaned_data if prop]
            count_main = len([v for v in main_values if v])
            if count_main > 1:
                raise ValidationError('Allowed 1 main image per project')
