from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Comment, Like, Post, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'post', 'created_at')
        read_only_fields = ('author', 'post')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'created_at')
        read_only_fields = ('user', 'post')


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'tags', 'is_published', 'created_at')


class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'content', 'author', 'tags',
            'is_published', 'created_at', 'updated_at',
            'comments', 'like_count',
        )

    def get_like_count(self, obj):
        return obj.likes.count()


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=False,
    )

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'tags', 'is_published')
