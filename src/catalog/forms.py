from collections import Counter

from django import forms
from django.core.exceptions import ValidationError


class ProductPropertyInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        """Check that properties are unique"""
        if self.is_valid():
            properties = [prop.get('property', '').title for prop in self.cleaned_data if prop]
            property_counter = Counter(properties)
            if [prop for prop, count in property_counter.items() if count > 1]:
                raise ValidationError('Property duplicates are not allowed')
