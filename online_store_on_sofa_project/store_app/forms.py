from django.forms import ModelForm
from .models import Product, ImageProduct, Comment


class AddNewProductBySuperuserForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'brand', 'rubric']


class AddImageNewProductBySuperuserForm(ModelForm):
    class Meta:
        model = ImageProduct
        fields = ['image', 'product']


