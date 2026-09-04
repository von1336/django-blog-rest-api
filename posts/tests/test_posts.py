import pytest
from rest_framework import status


@pytest.mark.django_db
class TestPostViewSet:
    def test_list_posts(self, api_client):
        response = api_client.get('/api/posts/')
        assert response.status_code == status.HTTP_200_OK

    def test_create_post_requires_auth(self, api_client, tag):
        response = api_client.post('/api/posts/', {
            'title': 'Test Post',
            'content': 'Test content',
            'tags': [tag.id],
            'is_published': True,
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_post_authenticated(self, auth_client, tag):
        response = auth_client.post('/api/posts/', {
            'title': 'Test Post',
            'content': 'Test content',
            'tags': [tag.id],
            'is_published': True,
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'Test Post'
        assert response.data['author'] is not None

    def test_update_post_only_author(self, auth_client, post, other_user):
        from rest_framework.authtoken.models import Token
        from rest_framework.test import APIClient

        other_token = Token.objects.create(user=other_user)
        other_client = APIClient()
        other_client.credentials(HTTP_AUTHORIZATION=f'Token {other_token.key}')

        response = other_client.patch(
            f'/api/posts/{post.id}/',
            {'title': 'Updated by other'},
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = auth_client.patch(
            f'/api/posts/{post.id}/',
            {'title': 'Updated by author'},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated by author'

    def test_delete_post_only_author(self, post, other_user):
        from rest_framework.authtoken.models import Token
        from rest_framework.test import APIClient

        other_token = Token.objects.create(user=other_user)
        other_client = APIClient()
        other_client.credentials(HTTP_AUTHORIZATION=f'Token {other_token.key}')

        response = other_client.delete(f'/api/posts/{post.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_like_post(self, auth_client, post):
        response = auth_client.post(f'/api/posts/{post.id}/like/')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['status'] == 'liked'

        response = auth_client.post(f'/api/posts/{post.id}/like/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'already liked'

    def test_unlike_post(self, auth_client, post, user):
        from posts.models import Like
        Like.objects.create(user=user, post=post)

        response = auth_client.post(f'/api/posts/{post.id}/unlike/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'unliked'
