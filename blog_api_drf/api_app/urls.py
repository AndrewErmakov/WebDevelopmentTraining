from django.urls import path
from rest_framework import routers
from .views import PostsListAPIView, PostCreateAPIView

router = routers.SimpleRouter()
router.register(r'posts', PostsListAPIView)

# URLs настраиваются автоматически роутером
urlpatterns = router.urls

# urlpatterns += [
#     path('create_post', PostCreateAPIView.as_view()),
# ]
