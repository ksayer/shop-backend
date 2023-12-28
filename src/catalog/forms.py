from collections import Counter

from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Property


class ProductPropertyInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        """Check that properties are unique"""
        if self.is_valid():
            properties = [prop.get('property', '').title for prop in self.cleaned_data if prop]
            property_counter = Counter(properties)
            if [prop for prop, count in property_counter.items() if count > 1]:
                raise ValidationError('Property duplicates are not allowed')


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'

    def clean_group(self):
        """Check that chosen group belongs to current property"""
        if self.is_valid():
            group = self.cleaned_data.get('group')
            if group.property_title and group.property_title != self.instance.get_title_display():
                raise ValidationError(f'Chosen group only for {group.property_title}')
        return group
