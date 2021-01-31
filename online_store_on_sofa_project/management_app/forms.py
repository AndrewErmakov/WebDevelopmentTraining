from django.forms import ModelForm
from store_app.models import Product, ImageProduct


class AddNewProductsForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'brand', 'rubric']


class AddImageForProductForm(ModelForm):
    class Meta:
        model = ImageProduct
        fields = ['image', 'product']
