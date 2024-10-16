from django import forms
from django_jsonform.widgets import JSONFormWidget

from .models import Category, Product, ProductVariant


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        product = self.instance
        if "attributes" in self.fields:
            if not product.category_id:
                self.fields["attributes"].widget.input_type = "hidden"
            else:
                self.fields["attributes"].widget = JSONFormWidget(
                    product.category.product_attributes_schema
                )


class ProductVariantAdminForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        product_variant = self.instance
        if "attributes" in self.fields:
            if not product_variant.product_id:
                self.fields["attributes"].widget.input_type = "hidden"
            else:
                self.fields["attributes"].widget = JSONFormWidget(
                    product_variant.product.category.variant_attributes_schema
                )
