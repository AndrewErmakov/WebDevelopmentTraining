from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import *
urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('contacts/', ContactsPage.as_view(), name='contacts'),
    path('product_details/<int:pk>/', ProductDetailsPage.as_view(), name='product_details'),
    path('products_by_rubric/<int:pk>/', ProductsByRubricPage.as_view(), name='products_by_rubric'),
    path('add_new_product', AddNewProductBySuperuser.as_view(), name='add_new_product'),
    # product page
    path('add_image_product', AddImageProductBySuperuser.as_view(), name='add_image_product'),
    path('add_new_comment', AddNewComment.as_view(), name='add_new_comment'),
    path('add_product_to_basket', AddProductToCart.as_view(), name='add_product_to_basket'),
    # cart page
    path('user_cart_page', UserCartPage.as_view(), name='user_cart_page'),
    path('delete_product_in_cart', DeleteProductInCart.as_view(), name='delete_product_in_cart'),
    path('reduce_count_products', ReduceCountProducts.as_view(), name='reduce_count_products'),
    path('increase_count_products', IncreaseCountProducts.as_view(), name='increase_count_products'),
    # ordering
    path('ordering', Ordering.as_view(), name='ordering'),
    path('order_created/<int:encrypted_order_num>/<int:key>/', OrderCreatedView.as_view(), name='order_created')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


