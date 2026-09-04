import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from posts.models import Post, Tag


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
    )


@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        username='otheruser',
        email='other@example.com',
        password='otherpass123',
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client(api_client, user):
    token, _ = Token.objects.get_or_create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return api_client


@pytest.fixture
def tag(db):
    return Tag.objects.create(name='Python', slug='python')


@pytest.fixture
def post(db, user, tag):
    post = Post.objects.create(
        title='Test Post',
        content='Test content',
        author=user,
        is_published=True,
    )
    post.tags.add(tag)
    return post
