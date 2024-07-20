from django import forms
from django.contrib import admin
from .models import Category, Product, ProductVariant
from django.db.models.fields.json import JSONField
from jsoneditor.forms import JSONEditor
import json

class DynamicProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []
        widgets = {
            'attributes': JSONEditor(
                init_options={"mode": "code", "modes": ["view", "tree", "code"]}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            category = self.instance.category
            self.add_dynamic_fields(category.product_attributes_schema)

    def add_dynamic_fields(self, schema, prefix="attributes_"):
        properties = schema.get('properties', {})
        # print(properties)
        for field, field_attrs in properties.items():
            # print(f'{field=}  |  {field_attrs=}')
            field_type = field_attrs.get('type')
            field_label = field_attrs.get('title', field)
            field_name = f'{prefix}{field}'

            if field_type == 'string':
                self.base_fields[field_name] = forms.CharField(label=field_label)
                self.fields[field_name] = forms.CharField(label=field_label)
            elif field_type == 'number':
                self.base_fields[field_name] = forms.FloatField(label=field_label)
                self.fields[field_name] = forms.FloatField(label=field_label)
            elif field_type == 'integer':
                self.base_fields[field_name] = forms.IntegerField(label=field_label)
                self.fields[field_name] = forms.IntegerField(label=field_label)
            elif field_type == 'object':
                self.add_dynamic_fields(field_attrs, prefix=f'{field_name}_')
            # Add more field types as needed

    def save(self, commit=True):
        instance = super().save(commit=False)
        attributes = {}
        for field in self.fields:
            if field.startswith('attributes_'):
                keys = field[len('attributes_'):].split('_')
                sub_dict = attributes
                for key in keys[:-1]:
                    if key not in sub_dict:
                        sub_dict[key] = {}
                    sub_dict = sub_dict[key]
                sub_dict[keys[-1]] = self.cleaned_data[field]
        instance.attributes = attributes
        if commit:
            instance.save()
        return instance

class DynamicProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        exclude = []

        widgets = {
            'attributes': JSONEditor(
                init_options={"mode": "code", "modes": ["view", "tree", "code"]}
            )
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            product = self.instance.product
            category = product.category

            self.add_dynamic_fields(category.variant_attributes_schema)

    def add_dynamic_fields(self, schema, prefix="attributes_"):
        properties = schema.get('properties', {})
        for field, field_attrs in properties.items():
            field_type = field_attrs.get('type')
            field_label = field_attrs.get('title', field)
            field_name = f'{prefix}{field}'

            if field_type == 'string':
                self.base_fields[field_name] = forms.CharField(label=field_label)
                self.fields[field_name] = forms.CharField(label=field_label)
            elif field_type == 'number':
                self.base_fields[field_name] = forms.FloatField(label=field_label)
                self.fields[field_name] = forms.FloatField(label=field_label)
            elif field_type == 'integer':
                self.base_fields[field_name] = forms.IntegerField(label=field_label)
                self.fields[field_name] = forms.IntegerField(label=field_label)
            elif field_type == 'object':
                self.add_dynamic_fields(field_attrs, prefix=f'{field_name}_')
            # Add more field types as needed

    def save(self, commit=True):
        instance = super().save(commit=False)
        attributes = {}
        for field in self.fields:
            if field.startswith('attributes_'):
                keys = field[len('attributes_'):].split('_')
                sub_dict = attributes
                for key in keys[:-1]:
                    if key not in sub_dict:
                        sub_dict[key] = {}
                    sub_dict = sub_dict[key]
                sub_dict[keys[-1]] = self.cleaned_data[field]
        instance.attributes = attributes
        if commit:
            instance.save()
        return instance
