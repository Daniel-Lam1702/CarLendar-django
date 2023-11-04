from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user_id.username', read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'body', 'user_id', 'username', 'created_at']