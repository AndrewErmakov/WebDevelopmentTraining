from django.conf import settings
from django.urls import path, re_path
from django.conf.urls.static import static
from .views import *
urlpatterns = [
    path('', HomepageView.as_view(), name='home'),

    path('product_details/<int:pk>/', ProductDetailsPageView.as_view(), name='product_details'),
    path('products_by_rubric/<int:pk>/', ProductsByRubricPageView.as_view(), name='products_by_rubric'),
    path('add_new_product', AddNewProductBySuperuserView.as_view(), name='add_new_product'),
    # product page
    path('add_image_product', AddImageProductBySuperuserView.as_view(), name='add_image_product'),
    path('add_new_comment', AddNewCommentView.as_view(), name='add_new_comment'),
    path('add_product_to_basket', AddProductToCartView.as_view(), name='add_product_to_basket'),
    # cart page
    path('user_cart_page', UserCartPageView.as_view(), name='user_cart_page'),
    path('delete_product_in_cart', DeleteProductInCartView.as_view(), name='delete_product_in_cart'),
    path('reduce_count_products', ReduceCountProductsView.as_view(), name='reduce_count_products'),
    path('increase_count_products', IncreaseCountProductsView.as_view(), name='increase_count_products'),
    # ordering
    path('ordering', OrderingView.as_view(), name='ordering'),
    path('order_created/<int:encrypted_order_num>/<int:key>/', OrderCreatedView.as_view(), name='order_created'),
    path('history_orders', HistoryOrdersView.as_view(), name='history_orders'),
    path('pdf_details_order/<str:num_str>', GeneratePdfOrderDetailsView.as_view(), name='pdf_details_order'),
    # footer
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
    path('feedback_form', FeedbackFormView.as_view(), name='feedback_form'),

    re_path(r'sorting_products/(?P<type_sorting>[a-z]+_[a-z]+)', ProductsBySortingView.as_view(),
            name='sorting_products'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


