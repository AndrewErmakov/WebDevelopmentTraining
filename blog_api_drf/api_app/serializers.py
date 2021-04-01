from posts_app.models import Post
from rest_framework import serializers


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
