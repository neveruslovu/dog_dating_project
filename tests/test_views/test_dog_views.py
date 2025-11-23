"""
Dog CRUD View Tests

Tests for dog profile creation, reading, updating, and deletion views.
"""

import pytest
from django.urls import reverse
from dogs.models import Dog


@pytest.mark.views
class TestDogListView:
    """Test dog listing view."""

    def test_dog_list_loads(self, client):
        """Test dog list page loads for any user."""
        response = client.get(reverse("dogs:dog_list"))
        assert response.status_code == 200

    def test_dog_list_shows_active_dogs(self, client, dog, inactive_dog):
        """Test dog list only shows active dogs."""
        response = client.get(reverse("dogs:dog_list"))
        assert response.status_code == 200
        dogs = response.context["page_obj"].object_list
        assert dog in dogs
        assert inactive_dog not in dogs

    def test_dog_list_pagination(self, client, multiple_dogs):
        """Test dog list is paginated."""
        response = client.get(reverse("dogs:dog_list"))
        assert response.status_code == 200
        assert "page_obj" in response.context
        # Default pagination is 12 per page
        assert len(response.context["page_obj"].object_list) <= 12

    def test_dog_list_search_by_breed(self, client, dog):
        """Test filtering dogs by breed."""
        response = client.get(reverse("dogs:dog_list"), {"breed": dog.breed})
        assert response.status_code == 200
        dogs = response.context["page_obj"].object_list
        assert all(d.breed == dog.breed or dog.breed in d.breed for d in dogs)

    def test_dog_list_filter_by_age(self, client):
        """Test filtering dogs by age range."""
        response = client.get(reverse("dogs:dog_list"), {"age_min": 2, "age_max": 5})
        assert response.status_code == 200

    def test_dog_list_filter_by_gender(self, client):
        """Test filtering dogs by gender."""
        response = client.get(reverse("dogs:dog_list"), {"gender": "M"})
        assert response.status_code == 200

    def test_dog_list_filter_by_size(self, client):
        """Test filtering dogs by size."""
        response = client.get(reverse("dogs:dog_list"), {"size": "L"})
        assert response.status_code == 200


@pytest.mark.views
class TestDogDetailView:
    """Test dog detail view."""

    def test_dog_detail_loads(self, client, dog):
        """Test dog detail page loads."""
        response = client.get(reverse("dogs:dog_detail", kwargs={"pk": dog.pk}))
        assert response.status_code == 200
        assert response.context["dog"] == dog

    def test_dog_detail_shows_owner_info(self, client, dog):
        """Test dog detail displays owner information."""
        response = client.get(reverse("dogs:dog_detail", kwargs={"pk": dog.pk}))
        assert response.status_code == 200
        assert dog.owner.username in str(response.content)

    def test_dog_detail_shows_edit_button_for_owner(self, authenticated_client, dog):
        """Test edit button shown to owner."""
        response = authenticated_client.get(
            reverse("dogs:dog_detail", kwargs={"pk": dog.pk})
        )
        assert response.status_code == 200
        assert response.context["can_edit"] is True

    def test_dog_detail_no_edit_button_for_others(self, client, dog, user2):
        """Test edit button not shown to non-owners."""
        client.force_login(user2)
        response = client.get(reverse("dogs:dog_detail", kwargs={"pk": dog.pk}))
        assert response.status_code == 200
        assert response.context["can_edit"] is False

    def test_dog_detail_shows_favorite_status(
        self, authenticated_client, dog, favorite
    ):
        """Test favorite status is displayed."""
        response = authenticated_client.get(
            reverse("dogs:dog_detail", kwargs={"pk": dog.pk})
        )
        assert "is_favorite" in response.context

    def test_inactive_dog_not_accessible(self, client, inactive_dog):
        """Test inactive dogs return 404."""
        response = client.get(
            reverse("dogs:dog_detail", kwargs={"pk": inactive_dog.pk})
        )
        assert response.status_code == 404


@pytest.mark.views
class TestDogCreateView:
    """Test dog creation view."""

    def test_dog_create_requires_login(self, client):
        """Test dog creation requires authentication."""
        response = client.get(reverse("dogs:dog_create"))
        assert response.status_code == 302

    def test_dog_create_page_loads(self, authenticated_client):
        """Test dog creation form loads."""
        response = authenticated_client.get(reverse("dogs:dog_create"))
        assert response.status_code == 200
        assert "form" in response.context

    def test_successful_dog_creation(self, authenticated_client, valid_dog_data):
        """Test creating a dog with valid data."""
        response = authenticated_client.post(
            reverse("dogs:dog_create"), data=valid_dog_data
        )

        assert response.status_code == 302
        assert Dog.objects.filter(name=valid_dog_data["name"]).exists()

    def test_dog_creation_sets_correct_owner(
        self, authenticated_client, user, valid_dog_data
    ):
        """Test created dog belongs to authenticated user."""
        authenticated_client.post(reverse("dogs:dog_create"), data=valid_dog_data)

        dog = Dog.objects.get(name=valid_dog_data["name"])
        assert dog.owner == user

    def test_dog_creation_with_invalid_age(self, authenticated_client, valid_dog_data):
        """Test dog creation fails with invalid age."""
        data = valid_dog_data.copy()
        data["age"] = 25  # Exceeds maximum

        response = authenticated_client.post(reverse("dogs:dog_create"), data=data)

        assert response.status_code == 200  # Form with errors
        assert not Dog.objects.filter(name=data["name"]).exists()


@pytest.mark.views
class TestDogUpdateView:
    """Test dog update view."""

    def test_dog_update_requires_login(self, client, dog):
        """Test dog update requires authentication."""
        response = client.get(reverse("dogs:dog_update", kwargs={"pk": dog.pk}))
        assert response.status_code == 302

    def test_dog_update_page_loads_for_owner(self, authenticated_client, dog):
        """Test update form loads for dog owner."""
        response = authenticated_client.get(
            reverse("dogs:dog_update", kwargs={"pk": dog.pk})
        )
        assert response.status_code == 200
        assert "form" in response.context

    def test_dog_update_forbidden_for_non_owner(self, client, dog, user2):
        """Test non-owner cannot update dog."""
        client.force_login(user2)
        response = client.get(reverse("dogs:dog_update", kwargs={"pk": dog.pk}))
        assert response.status_code == 404  # get_object_or_404 with owner check

    def test_successful_dog_update(self, authenticated_client, dog):
        """Test updating dog with valid data."""
        new_description = "Updated description"
        response = authenticated_client.post(
            reverse("dogs:dog_update", kwargs={"pk": dog.pk}),
            data={
                "name": dog.name,
                "breed": dog.breed,
                "age": 5,  # Changed
                "gender": dog.gender,
                "size": dog.size,
                "temperament": dog.temperament,
                "looking_for": dog.looking_for,
                "description": new_description,
            },
        )

        assert response.status_code == 302
        dog.refresh_from_db()
        assert dog.age == 5
        assert dog.description == new_description


@pytest.mark.views
class TestDogDeleteView:
    """Test dog deletion view."""

    def test_dog_delete_requires_login(self, client, dog):
        """Test dog deletion requires authentication."""
        response = client.get(reverse("dogs:dog_delete", kwargs={"pk": dog.pk}))
        assert response.status_code == 302

    def test_dog_delete_confirmation_page_loads(self, authenticated_client, dog):
        """Test delete confirmation page loads for owner."""
        response = authenticated_client.get(
            reverse("dogs:dog_delete", kwargs={"pk": dog.pk})
        )
        assert response.status_code == 200
        assert "dog" in response.context

    def test_dog_delete_forbidden_for_non_owner(self, client, dog, user2):
        """Test non-owner cannot delete dog."""
        client.force_login(user2)
        response = client.get(reverse("dogs:dog_delete", kwargs={"pk": dog.pk}))
        assert response.status_code == 404

    def test_successful_dog_deletion(self, authenticated_client, dog):
        """Test deleting a dog."""
        dog_id = dog.id
        response = authenticated_client.post(
            reverse("dogs:dog_delete", kwargs={"pk": dog.pk})
        )

        assert response.status_code == 302
        assert not Dog.objects.filter(id=dog_id).exists()


@pytest.mark.views
class TestMatchesListView:
    """Test matches listing view."""

    def test_matches_list_requires_login(self, client):
        """Test matches list requires authentication."""
        response = client.get(reverse("dogs:matches_list"))
        assert response.status_code == 302

    def test_matches_list_loads(self, authenticated_client):
        """Test matches list page loads."""
        response = authenticated_client.get(reverse("dogs:matches_list"))
        assert response.status_code == 200
        assert "matches" in response.context

    def test_matches_list_shows_user_matches(self, authenticated_client, pending_match):
        """Test matches list shows user's matches."""
        response = authenticated_client.get(reverse("dogs:matches_list"))
        assert response.status_code == 200
        assert pending_match in response.context["matches"]

    def test_matches_list_pagination(self, authenticated_client):
        """Test matches are paginated."""
        response = authenticated_client.get(reverse("dogs:matches_list"))
        assert response.status_code == 200
        assert "page_obj" in response.context


@pytest.mark.views
class TestFavoritesListView:
    """Test favorites listing view."""

    def test_favorites_list_requires_login(self, client):
        """Test favorites list requires authentication."""
        response = client.get(reverse("dogs:favorites_list"))
        assert response.status_code == 302

    def test_favorites_list_loads(self, authenticated_client):
        """Test favorites list page loads."""
        response = authenticated_client.get(reverse("dogs:favorites_list"))
        assert response.status_code == 200
        assert "favorites" in response.context

    def test_favorites_list_shows_user_favorites(self, authenticated_client, favorite):
        """Test favorites list shows user's favorites."""
        response = authenticated_client.get(reverse("dogs:favorites_list"))
        assert response.status_code == 200
        assert favorite in response.context["favorites"]

    def test_favorites_list_pagination(self, authenticated_client):
        """Test favorites are paginated."""
        response = authenticated_client.get(reverse("dogs:favorites_list"))
        assert response.status_code == 200
        assert "page_obj" in response.context
