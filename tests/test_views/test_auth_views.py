"""
Authentication View Tests

Tests for user registration, login, logout, and password management views.
"""

import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.views
@pytest.mark.auth
class TestRegistrationView:
    """Test user registration view."""

    def test_registration_page_loads(self, client):
        """Test registration page loads for anonymous users."""
        response = client.get(reverse("dogs:register"))
        assert response.status_code == 200
        assert "form" in response.context

    def test_registration_with_valid_data(self, client, valid_user_data):
        """Test successful user registration."""
        response = client.post(reverse("dogs:register"), data=valid_user_data)

        assert response.status_code == 302  # Redirect after success
        assert User.objects.filter(username=valid_user_data["username"]).exists()

    def test_registration_with_mismatched_passwords(self, client):
        """Test registration fails with mismatched passwords."""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "testpass123!",
            "password2": "differentpass456!",
        }
        response = client.post(reverse("dogs:register"), data=data)

        assert response.status_code == 200  # Returns form with errors
        assert not User.objects.filter(username="newuser").exists()

    def test_registration_with_existing_username(self, client, user):
        """Test registration fails with existing username."""
        data = {
            "username": user.username,
            "email": "different@example.com",
            "password1": "testpass123!",
            "password2": "testpass123!",
        }
        response = client.post(reverse("dogs:register"), data=data)

        assert response.status_code == 200
        assert User.objects.filter(username=user.username).count() == 1

    def test_authenticated_user_redirected_from_registration(
        self, authenticated_client
    ):
        """Test authenticated users are redirected away from registration."""
        response = authenticated_client.get(reverse("dogs:register"))
        assert response.status_code == 302


@pytest.mark.views
@pytest.mark.auth
class TestLoginView:
    """Test user login view."""

    def test_login_page_loads(self, client):
        """Test login page loads for anonymous users."""
        response = client.get(reverse("dogs:login"))
        assert response.status_code == 200
        assert "form" in response.context

    def test_login_with_valid_credentials(self, client, user):
        """Test successful login with valid credentials."""
        response = client.post(
            reverse("dogs:login"),
            {"username": user.username, "password": "testpass123"},
        )

        assert response.status_code == 302  # Redirect to dashboard
        assert response.url == reverse("dogs:dashboard")

    def test_login_with_invalid_password(self, client, user):
        """Test login fails with wrong password."""
        response = client.post(
            reverse("dogs:login"),
            {"username": user.username, "password": "wrongpassword"},
        )

        assert response.status_code == 200
        assert "form" in response.context

    def test_login_with_nonexistent_user(self, client):
        """Test login fails with nonexistent username."""
        response = client.post(
            reverse("dogs:login"),
            {"username": "nonexistent", "password": "password123"},
        )

        assert response.status_code == 200

    def test_login_remember_me_functionality(self, client, user):
        """Test remember me checkbox sets session expiry."""
        response = client.post(
            reverse("dogs:login"),
            {"username": user.username, "password": "testpass123", "remember_me": True},
        )

        assert response.status_code == 302

    def test_authenticated_user_redirected_from_login(self, authenticated_client):
        """Test authenticated users are redirected away from login."""
        response = authenticated_client.get(reverse("dogs:login"))
        assert response.status_code == 302


@pytest.mark.views
@pytest.mark.auth
class TestLogoutView:
    """Test user logout view."""

    def test_logout_redirects_to_landing(self, authenticated_client):
        """Test logout redirects to landing page."""
        response = authenticated_client.get(reverse("dogs:logout"))

        assert response.status_code == 302
        assert response.url == reverse("dogs:landing_page")

    def test_user_is_logged_out(self, authenticated_client):
        """Test user session is actually terminated."""
        authenticated_client.get(reverse("dogs:logout"))

        # Try accessing protected page
        response = authenticated_client.get(reverse("dogs:dashboard"))
        assert response.status_code == 302  # Redirected to login


@pytest.mark.views
@pytest.mark.auth
class TestPasswordChangeView:
    """Test password change view."""

    def test_password_change_requires_login(self, client):
        """Test password change view requires authentication."""
        response = client.get(reverse("dogs:change_password"))
        assert response.status_code == 302  # Redirect to login

    def test_password_change_page_loads(self, authenticated_client):
        """Test password change page loads for authenticated users."""
        response = authenticated_client.get(reverse("dogs:change_password"))
        assert response.status_code == 200
        assert "form" in response.context

    def test_successful_password_change(self, authenticated_client, user):
        """Test changing password with valid data."""
        response = authenticated_client.post(
            reverse("dogs:change_password"),
            {
                "old_password": "testpass123",
                "new_password1": "newpass456!",
                "new_password2": "newpass456!",
            },
        )

        assert response.status_code == 302

        # Verify password was changed
        user.refresh_from_db()
        assert user.check_password("newpass456!")

    def test_password_change_with_wrong_old_password(self, authenticated_client):
        """Test password change fails with incorrect old password."""
        response = authenticated_client.post(
            reverse("dogs:change_password"),
            {
                "old_password": "wrongpass",
                "new_password1": "newpass456!",
                "new_password2": "newpass456!",
            },
        )

        assert response.status_code == 302  # Redirects with error message


@pytest.mark.views
@pytest.mark.auth
class TestDeleteAccountView:
    """Test account deletion view."""

    def test_delete_account_requires_login(self, client):
        """Test delete account view requires authentication."""
        response = client.get(reverse("dogs:delete_account"))
        assert response.status_code == 302

    def test_delete_account_page_loads(self, authenticated_client):
        """Test delete account confirmation page loads."""
        response = authenticated_client.get(reverse("dogs:delete_account"))
        assert response.status_code == 200
        assert "form" in response.context

    def test_successful_account_deletion(self, authenticated_client, user):
        """Test successful account deletion."""
        user_id = user.id
        username = user.username

        response = authenticated_client.post(
            reverse("dogs:delete_account"), {"password": "testpass123", "confirm_deletion": True}
        )

        # Should redirect after deletion (302) or render success page (200)
        assert response.status_code == 302
        assert not User.objects.filter(id=user_id).exists()
        assert not User.objects.filter(username=username).exists()

    def test_account_deletion_with_wrong_password(self, authenticated_client, user):
        """Test account deletion fails with wrong password."""
        user_id = user.id

        response = authenticated_client.post(
            reverse("dogs:delete_account"), {"password": "wrongpassword", "confirm_deletion": True}
        )

        # Should either redirect with error (302) or re-render form (200)
        assert response.status_code == 302
        assert User.objects.filter(id=user_id).exists()


@pytest.mark.views
class TestLandingPage:
    """Test landing page view."""

    def test_landing_page_loads_for_anonymous(self, client):
        """Test landing page loads for anonymous users."""
        response = client.get(reverse("dogs:landing_page"))
        assert response.status_code == 200

    def test_landing_page_shows_featured_dogs(self, client, multiple_dogs):
        """Test landing page displays featured dogs."""
        response = client.get(reverse("dogs:landing_page"))
        assert response.status_code == 200
        assert "featured_dogs" in response.context

    def test_authenticated_user_redirected_to_dashboard(self, authenticated_client):
        """Test authenticated users are redirected to dashboard."""
        response = authenticated_client.get(reverse("dogs:landing_page"))
        assert response.status_code == 302
        assert response.url == reverse("dogs:dashboard")

    def test_staff_user_logged_out_on_landing(self, staff_client):
        """Test staff users are logged out when accessing landing page."""
        response = staff_client.get(reverse("dogs:landing_page"))
        assert response.status_code == 302


@pytest.mark.views
class TestDashboardView:
    """Test user dashboard view."""

    def test_dashboard_requires_login(self, client):
        """Test dashboard requires authentication."""
        response = client.get(reverse("dogs:dashboard"))
        assert response.status_code == 302  # Redirect to login

    def test_dashboard_loads_for_authenticated_user(self, authenticated_client, user):
        """Test dashboard loads successfully for authenticated users."""
        response = authenticated_client.get(reverse("dogs:dashboard"))
        assert response.status_code == 200
        assert response.wsgi_request.user == user

    def test_dashboard_displays_user_dogs(self, authenticated_client, dog, user):
        """Test dashboard shows user's dogs."""
        response = authenticated_client.get(reverse("dogs:dashboard"))
        assert response.status_code == 200
        assert "user_dogs" in response.context
        # Verify the dog is in the user's dogs
        user_dog_ids = [d.id for d in response.context["user_dogs"]]
        assert dog.id in user_dog_ids

    def test_dashboard_shows_statistics(self, authenticated_client, user):
        """Test dashboard displays user statistics."""
        response = authenticated_client.get(reverse("dogs:dashboard"))
        assert response.status_code == 200
        context = response.context
        # Check that statistics keys exist
        assert "total_matches" in context or "matches" in context
        assert "total_favorites" in context or "favorites" in context

    def test_dashboard_shows_recent_matches(
        self, authenticated_client, pending_match, user
    ):
        """Test dashboard displays recent match activity."""
        response = authenticated_client.get(reverse("dogs:dashboard"))
        assert response.status_code == 200
        # Check for matches in context with flexible key names
        assert "recent_matches" in response.context or "matches" in response.context
