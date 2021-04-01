from django.urls import path

from posts_app.views import PostsListView, PostDetailView, PostCreateView

urlpatterns = [
    path('', PostsListView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('create_post', PostCreateView.as_view())
]
