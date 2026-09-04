import pytest
from rest_framework import status


@pytest.mark.django_db
class TestCommentViewSet:
    def test_add_comment(self, auth_client, post):
        response = auth_client.post(
            f'/api/posts/{post.id}/comments/',
            {'text': 'Great post!'},
            format='json',
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['text'] == 'Great post!'
        assert response.data['author'] is not None

    def test_list_comments_for_post(self, api_client, post, auth_client):
        auth_client.post(
            f'/api/posts/{post.id}/comments/',
            {'text': 'First comment'},
            format='json',
        )
        auth_client.post(
            f'/api/posts/{post.id}/comments/',
            {'text': 'Second comment'},
            format='json',
        )

        response = api_client.get(f'/api/posts/{post.id}/comments/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
