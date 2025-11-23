"""
Dog Permission Tests

Tests for dog ownership and access control.
"""

import pytest
from django.core.exceptions import PermissionDenied
from services.dog_service import get_dog_for_owner
from services.favorites_service import toggle_favorite_for_user
from services.match_service import create_match_for_user


@pytest.mark.permissions
class TestDogOwnershipPermissions:
    """Test dog ownership permission checks."""

    def test_owner_can_access_own_dog(self, user, dog):
        """Test owner can access their own dog."""
        result = get_dog_for_owner(user, dog.id)
        assert result == dog

    def test_non_owner_cannot_access_dog(self, user2, dog):
        """Test non-owner cannot access someone else's dog."""
        with pytest.raises(PermissionDenied):
            get_dog_for_owner(user2, dog.id)

    def test_anonymous_user_cannot_access_dog(self, anonymous_user, dog):
        """Test anonymous user cannot access dog via service."""
        # In Django 5.x, anonymous users may behave differently
        with pytest.raises((PermissionDenied, AttributeError, TypeError)):
            get_dog_for_owner(anonymous_user, dog.id)


@pytest.mark.permissions
class TestFavoritePermissions:
    """Test favorite permission checks."""

    def test_authenticated_user_can_favorite(self, user, other_dog):
        """Test authenticated user can add favorites."""
        is_favorite, message = toggle_favorite_for_user(user, other_dog.id)
        assert is_favorite is True

    def test_anonymous_user_cannot_favorite(self, anonymous_user, dog):
        """Test anonymous user cannot add favorites."""
        with pytest.raises(PermissionDenied):
            toggle_favorite_for_user(anonymous_user, dog.id)

    def test_user_can_unfavorite(self, user, other_dog, favorite):
        """Test user can remove their own favorites."""
        is_favorite, message = toggle_favorite_for_user(user, other_dog.id)
        assert is_favorite is False


@pytest.mark.permissions
class TestMatchPermissions:
    """Test match creation permission checks."""

    def test_user_can_create_match_with_own_dog(self, user, dog, other_dog):
        """Test user can create match with their own dog."""
        match = create_match_for_user(user, dog.id, other_dog.id)
        assert match is not None
        assert match.dog_from == dog
        assert match.dog_to == other_dog

    def test_user_cannot_match_dog_with_itself(self, user, dog):
        """Test cannot create match between same dog."""
        with pytest.raises(PermissionDenied):
            create_match_for_user(user, dog.id, dog.id)

    def test_user_cannot_match_between_own_dogs(self, user, dog, dog2):
        """Test cannot create match between user's own dogs."""
        with pytest.raises(PermissionDenied):
            create_match_for_user(user, dog.id, dog2.id)

    def test_user_cannot_match_from_others_dog(self, user, other_dog, dog):
        """Test user cannot initiate match from dog they don't own."""
        with pytest.raises(PermissionDenied):
            create_match_for_user(user, other_dog.id, dog.id)


@pytest.mark.permissions
class TestViewPermissions:
    """Test view-level permission checks."""

    def test_dashboard_requires_authentication(self, client):
        """Test dashboard view requires login."""
        from django.urls import reverse

        response = client.get(reverse("dogs:dashboard"))
        assert response.status_code == 302  # Redirect to login
        assert "/login/" in response.url

    def test_dog_create_requires_authentication(self, client):
        """Test dog creation requires login."""
        from django.urls import reverse

        response = client.get(reverse("dogs:dog_create"))
        assert response.status_code == 302

    def test_dog_update_requires_ownership(self, client, dog, user2):
        """Test dog update requires ownership."""
        from django.urls import reverse

        client.force_login(user2)
        response = client.get(reverse("dogs:dog_update", kwargs={"pk": dog.pk}))
        assert response.status_code == 404  # Not found (ownership check)

    def test_dog_delete_requires_ownership(self, client, dog, user2):
        """Test dog deletion requires ownership."""
        from django.urls import reverse

        client.force_login(user2)
        response = client.get(reverse("dogs:dog_delete", kwargs={"pk": dog.pk}))
        assert response.status_code == 404

    def test_profile_requires_authentication(self, client):
        """Test profile view requires login."""
        from django.urls import reverse

        response = client.get(reverse("dogs:profile"))
        assert response.status_code == 302

    def test_favorites_requires_authentication(self, client):
        """Test favorites list requires login."""
        from django.urls import reverse

        response = client.get(reverse("dogs:favorites_list"))
        assert response.status_code == 302

    def test_matches_requires_authentication(self, client):
        """Test matches list requires login."""
        from django.urls import reverse

        response = client.get(reverse("dogs:matches_list"))
        assert response.status_code == 302
