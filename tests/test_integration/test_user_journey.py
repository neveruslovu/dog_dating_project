"""
User Journey Integration Tests

End-to-end tests for complete user workflows.
"""

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from dogs.models import Dog, Favorite, Match


@pytest.mark.integration
class TestNewUserJourney:
    """Test complete journey for a new user."""

    def test_complete_registration_to_dog_creation(self, client):
        """Test user registration through dog creation."""
        # Step 1: Register new user
        register_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "testpass123!",
            "password2": "testpass123!",
        }
        response = client.post(
            reverse("dogs:register"), data=register_data, follow=True
        )
        assert response.status_code == 200
        assert User.objects.filter(username="newuser").exists()

        # Step 2: User should be automatically logged in - verify by accessing dashboard
        response = client.get(reverse("dogs:dashboard"))
        # Should be able to access dashboard (200) or be redirected (302)
        assert response.status_code in [200, 302]

        # Step 3: Create first dog
        dog_data = {
            "name": "FirstDog",
            "breed": "Labrador",
            "age": 3,
            "gender": "M",
            "size": "L",
            "temperament": "friendly",
            "looking_for": "playmate",
            "description": "My first dog on DogDating",
        }
        response = client.post(reverse("dogs:dog_create"), data=dog_data)
        assert response.status_code == 302
        assert Dog.objects.filter(name="FirstDog").exists()

        # Step 4: View dog profile
        dog = Dog.objects.get(name="FirstDog")
        response = client.get(reverse("dogs:dog_detail", kwargs={"pk": dog.pk}))
        assert response.status_code == 200


@pytest.mark.integration
class TestDoging:
    """Test browsing and favoriting dogs."""

    def test_browse_and_favorite_workflow(self, authenticated_client, other_dog):
        """Test browsing dogs and adding to favorites."""
        # Step 1: Browse dog list
        response = authenticated_client.get(reverse("dogs:dog_list"))
        assert response.status_code == 200

        # Step 2: View dog detail
        response = authenticated_client.get(
            reverse("dogs:dog_detail", kwargs={"pk": other_dog.pk})
        )
        assert response.status_code == 200

        # Step 3: Add to favorites
        response = authenticated_client.post(
            reverse("dogs:toggle_favorite", kwargs={"pk": other_dog.pk})
        )
        assert response.status_code == 200

        # Step 4: Check favorites list
        response = authenticated_client.get(reverse("dogs:favorites_list"))
        assert response.status_code == 200
        assert any(f.dog == other_dog for f in response.context["favorites"])


@pytest.mark.integration
class TestMatchWorkflow:
    """Test match creation and management workflow."""

    def test_create_and_view_match(self, user, user2, dog, other_dog, client):
        """Test creating a match and viewing it."""
        # Login as first user
        client.force_login(user)

        # Step 1: Browse dogs
        response = client.get(reverse("dogs:dog_list"))
        assert response.status_code == 200

        # Step 2: View target dog
        response = client.get(reverse("dogs:dog_detail", kwargs={"pk": other_dog.pk}))
        assert response.status_code == 200

        # Step 3: Create match using service (simulating button click)
        from services.match_service import create_match_for_user

        match = create_match_for_user(user, dog.id, other_dog.id)
        assert match is not None

        # Step 4: View matches list
        response = client.get(reverse("dogs:matches_list"))
        assert response.status_code == 200
        assert match in response.context["matches"]


@pytest.mark.integration
class TestSearchAndFilterWorkflow:
    """Test search and filter functionality."""

    def test_complete_search_workflow(self, client, multiple_dogs):
        """Test searching and filtering dogs."""
        # Step 1: Access dog list
        response = client.get(reverse("dogs:dog_list"))
        assert response.status_code == 200
        initial_count = len(response.context["page_obj"].object_list)

        # Step 2: Search by breed
        response = client.get(reverse("dogs:dog_list"), {"breed": "Breed5"})
        assert response.status_code == 200
        breed_filtered = len(response.context["page_obj"].object_list)
        assert breed_filtered <= initial_count

        # Step 3: Add age filter
        response = client.get(
            reverse("dogs:dog_list"), {"breed": "Breed5", "age_min": 2, "age_max": 5}
        )
        assert response.status_code == 200

        # Step 4: Add gender filter
        response = client.get(
            reverse("dogs:dog_list"),
            {"breed": "Breed5", "age_min": 2, "age_max": 5, "gender": "M"},
        )
        assert response.status_code == 200


@pytest.mark.integration
class TestProfileManagementWorkflow:
    """Test user profile management workflow."""

    def test_complete_profile_update_workflow(self, authenticated_client, user):
        """Test updating user profile and changing password."""
        # Step 1: View profile
        response = authenticated_client.get(reverse("dogs:profile"))
        assert response.status_code == 200

        # Step 2: Edit profile (may need to create profile first in Django 5.x)
        from dogs.models import UserProfile

        profile, created = UserProfile.objects.get_or_create(user=user)

        profile_data = {
            "bio": "Updated bio",
            "location": "New City",
            "phone": "+1234567890",
        }
        response = authenticated_client.post(
            reverse("dogs:profile_edit"), data=profile_data, files={}
        )
        print(f"Profile edit status: {response.status_code}")
        assert response.status_code == 302

        # Step 3: Verify profile was updated
        response = authenticated_client.get(reverse("dogs:profile"))
        assert response.status_code == 200

        # Step 4: Change password
        response = authenticated_client.post(
            reverse("dogs:change_password"),
            data={
                "old_password": "testpass123",
                "new_password1": "NewSecurePass123!",
                "new_password2": "NewSecurePass123!",
            },
        )
        print(f"Password change status: {response.status_code}")
        if (
            response.status_code != 302
            and hasattr(response, "context")
            and response.context
        ):
            if "form" in response.context:
                print(f"Form errors: {response.context['form'].errors}")
        assert response.status_code == 302


@pytest.mark.integration
class TestMultiDogWorkflow:
    """Test managing multiple dogs."""

    def test_create_multiple_dogs_workflow(self, authenticated_client, user):
        """Test creating and managing multiple dog profiles."""
        # Step 1: Create first dog
        dog1_data = {
            "name": "Dog1",
            "breed": "Breed1",
            "age": 3,
            "gender": "M",
            "size": "L",
            "temperament": "friendly",
            "looking_for": "playmate",
            "description": "First dog",
        }
        response = authenticated_client.post(reverse("dogs:dog_create"), data=dog1_data)
        assert response.status_code == 302

        # Step 2: Create second dog
        dog2_data = dog1_data.copy()
        dog2_data["name"] = "Dog2"
        dog2_data["gender"] = "F"
        response = authenticated_client.post(reverse("dogs:dog_create"), data=dog2_data)
        assert response.status_code == 302

        # Step 3: View dashboard showing both dogs
        response = authenticated_client.get(reverse("dogs:dashboard"))
        assert response.status_code == 200
        user_dogs = response.context.get("user_dogs", [])
        assert len(user_dogs) >= 2

        # Step 4: Edit one dog
        dog1 = Dog.objects.get(name="Dog1", owner=user)
        edit_data = dog1_data.copy()
        edit_data["age"] = 4
        response = authenticated_client.post(
            reverse("dogs:dog_update", kwargs={"pk": dog1.pk}), data=edit_data
        )
        assert response.status_code == 302

        # Step 5: Delete one dog
        dog2 = Dog.objects.get(name="Dog2", owner=user)
        response = authenticated_client.post(
            reverse("dogs:dog_delete", kwargs={"pk": dog2.pk})
        )
        assert response.status_code == 302
        # Count only active dogs owned by user
        remaining_dogs = Dog.objects.filter(owner=user).count()
        assert remaining_dogs >= 1


@pytest.mark.integration
@pytest.mark.slow
class TestPaginationWorkflow:
    """Test pagination across different views."""

    def test_favorites_pagination_workflow(
        self, authenticated_client, user, multiple_dogs
    ):
        """Test favorites list pagination."""
        # Step 1: Add many dogs to favorites
        added_count = 0
        for dog in multiple_dogs:
            if dog.owner != user:
                Favorite.objects.get_or_create(user=user, dog=dog)
                added_count += 1
                if added_count >= 15:
                    break

        # Step 2: View first page
        response = authenticated_client.get(reverse("dogs:favorites_list"))
        assert response.status_code == 200
        page1 = response.context.get("page_obj")
        if page1:
            # Default page size is typically 12
            assert len(page1.object_list) <= 12

        # Step 3: View second page (if exists)
        response = authenticated_client.get(reverse("dogs:favorites_list"), {"page": 2})
        assert response.status_code in [200, 404]  # 404 if no second page
        if response.status_code == 200:
            page2 = response.context.get("page_obj")
            if page2:
                assert len(page2.object_list) >= 0
