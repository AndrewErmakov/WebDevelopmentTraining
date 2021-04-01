from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from api_app.serializers import PostsSerializer
from posts_app.models import Post


class PostsListAPIView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer


class PostCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostsSerializer

