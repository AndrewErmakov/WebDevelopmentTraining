from django.forms import ModelForm
from .models import Product


class AddNewProductBySuperuserForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'brand', 'rubric', 'image_product']
