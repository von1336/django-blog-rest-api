from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, PostViewSet, TagViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'tags', TagViewSet, basename='tag')

comments_router = DefaultRouter()
comments_router.register(r'comments', CommentViewSet, basename='post-comment')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_pk>/', include(comments_router.urls)),
]
