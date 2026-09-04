from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Comment, Like, Post, Tag
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    PostCreateUpdateSerializer,
    PostDetailSerializer,
    PostListSerializer,
    TagSerializer,
)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'content']

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return PostCreateUpdateSerializer
        return PostDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                qs = Post.objects.all()
            else:
                qs = Post.objects.filter(Q(is_published=True) | Q(author=user))
        else:
            qs = Post.objects.filter(is_published=True)

        tag_slug = self.request.query_params.get('tag')
        if tag_slug:
            qs = qs.filter(tags__slug=tag_slug)
        return qs.distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        _, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'already liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
        if deleted:
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        return Response({'status': 'was not liked'}, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        serializer.save(author=self.request.user, post=post)
