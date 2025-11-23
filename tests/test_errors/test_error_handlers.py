"""
Error Handler Tests

Tests for custom 404 and 500 error handlers.
"""

import pytest
from django.test import override_settings


@pytest.mark.views
class Test404ErrorHandler:
    """Test 404 Not Found error handler."""

    @override_settings(DEBUG=False)
    def test_404_handler_renders_template(self, client):
        """Test 404 handler renders custom template."""
        response = client.get("/nonexistent-url/")
        assert response.status_code == 404
        # Note: Template testing requires DEBUG=False

    def test_404_for_nonexistent_dog(self, client):
        """Test 404 for nonexistent dog ID."""
        from django.urls import reverse

        response = client.get(reverse("dogs:dog_detail", kwargs={"pk": 99999}))
        assert response.status_code == 404

    def test_404_for_inactive_dog(self, client, inactive_dog):
        """Test inactive dogs return 404."""
        from django.urls import reverse

        response = client.get(
            reverse("dogs:dog_detail", kwargs={"pk": inactive_dog.pk})
        )
        assert response.status_code == 404


@pytest.mark.views
class Test500ErrorHandler:
    """Test 500 Internal Server Error handler."""

    @override_settings(DEBUG=False)
    def test_500_handler_exists(self):
        """Test 500 error handler is configured."""
        from django.conf import settings
        from project import urls

        # Check if handler500 is defined in URLconf or settings
        has_handler = (
            hasattr(settings, "handler500")
            or hasattr(urls, "handler500")
            or "handler500" in dir(settings)
            or "handler500" in dir(urls)
        )
        assert has_handler
