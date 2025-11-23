"""
AJAX Endpoint Tests

Tests for AJAX endpoints like favorite toggle.
"""

import pytest
import json
from django.urls import reverse
from dogs.models import Favorite


@pytest.mark.api
class TestToggleFavoriteEndpoint:
    """Test favorite toggle AJAX endpoint."""

    def test_toggle_favorite_requires_login(self, client, dog):
        """Test endpoint requires authentication."""
        response = client.post(reverse("dogs:toggle_favorite", kwargs={"pk": dog.pk}))
        assert response.status_code == 403  # Forbidden for anonymous users

    def test_toggle_favorite_requires_post(self, authenticated_client, other_dog):
        """Test endpoint only accepts POST requests."""
        response = authenticated_client.get(
            reverse("dogs:toggle_favorite", kwargs={"pk": other_dog.pk})
        )
        assert response.status_code == 403  # Forbidden for GET

    def test_toggle_favorite_adds_to_favorites(
        self, authenticated_client, other_dog, user
    ):
        """Test adding dog to favorites."""
        response = authenticated_client.post(
            reverse("dogs:toggle_favorite", kwargs={"pk": other_dog.pk})
        )

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["is_favorite"] is True
        assert Favorite.objects.filter(user=user, dog=other_dog).exists()

    def test_toggle_favorite_removes_from_favorites(
        self, authenticated_client, other_dog, user, favorite
    ):
        """Test removing dog from favorites."""
        # favorite fixture already created favorite for user
        response = authenticated_client.post(
            reverse("dogs:toggle_favorite", kwargs={"pk": other_dog.pk})
        )

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["is_favorite"] is False
        assert not Favorite.objects.filter(user=user, dog=other_dog).exists()

    def test_toggle_favorite_with_nonexistent_dog(self, authenticated_client):
        """Test toggling favorite for nonexistent dog."""
        response = authenticated_client.post(
            reverse("dogs:toggle_favorite", kwargs={"pk": 99999})
        )
        assert response.status_code == 404

    def test_toggle_favorite_returns_json(self, authenticated_client, other_dog):
        """Test endpoint returns JSON response."""
        response = authenticated_client.post(
            reverse("dogs:toggle_favorite", kwargs={"pk": other_dog.pk})
        )

        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"

        data = json.loads(response.content)
        assert "is_favorite" in data
        assert "message" in data

    def test_toggle_favorite_multiple_times(
        self, authenticated_client, other_dog, user
    ):
        """Test toggling favorite multiple times works correctly."""
        # Add to favorites
        response1 = authenticated_client.post(
            reverse("dogs:toggle_favorite", kwargs={"pk": other_dog.pk})
        )
        data1 = json.loads(response1.content)
        assert data1["is_favorite"] is True

        # Remove from favorites
        response2 = authenticated_client.post(
            reverse("dogs:toggle_favorite", kwargs={"pk": other_dog.pk})
        )
        data2 = json.loads(response2.content)
        assert data2["is_favorite"] is False

        # Add again
        response3 = authenticated_client.post(
            reverse("dogs:toggle_favorite", kwargs={"pk": other_dog.pk})
        )
        data3 = json.loads(response3.content)
        assert data3["is_favorite"] is True
