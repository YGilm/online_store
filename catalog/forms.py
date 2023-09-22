from django import forms
from django.core.exceptions import ValidationError
from .models import *

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')
        if any(word in product_name for word in FORBIDDEN_WORDS):
            raise ValidationError('В названии продукта содержатся запрещенные слова.')
        return product_name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if any(word in description for word in FORBIDDEN_WORDS):
            raise ValidationError('В описании продукта содержатся запрещенные слова.')
        return description


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = ['version_number', 'version_name', 'is_current']

