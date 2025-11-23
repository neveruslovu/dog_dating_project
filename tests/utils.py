"""
Test Utilities and Helper Functions

Common utilities for test setup, assertions, and data generation.
"""

from typing import Dict, Any, List
from django.contrib.auth.models import User
from dogs.models import Dog, Match, Favorite
from django.core.files.uploadedfile import SimpleUploadedFile


# ============================================================================
# Test Data Generators
# ============================================================================


def create_test_image(filename="test.jpg", content_type="image/jpeg", size=1024):
    """
    Create a simple test image file.

    Args:
        filename: Name of the file
        content_type: MIME type
        size: Size in bytes

    Returns:
        SimpleUploadedFile instance
    """
    content = b"x" * size
    return SimpleUploadedFile(filename, content, content_type=content_type)


def create_valid_dog_data(**overrides) -> Dict[str, Any]:
    """
    Create valid dog form data with optional overrides.

    Args:
        **overrides: Fields to override in the default data

    Returns:
        Dictionary of dog form data
    """
    data = {
        "name": "TestDog",
        "breed": "Test Breed",
        "age": 3,
        "gender": "M",
        "size": "M",
        "temperament": "friendly",
        "looking_for": "playmate",
        "description": "A test dog for testing purposes",
    }
    data.update(overrides)
    return data


def create_valid_user_data(**overrides) -> Dict[str, Any]:
    """
    Create valid user registration data with optional overrides.

    Args:
        **overrides: Fields to override

    Returns:
        Dictionary of user registration data
    """
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password1": "testpass123!",
        "password2": "testpass123!",
    }
    data.update(overrides)
    return data


# ============================================================================
# Assertion Helpers
# ============================================================================


def assert_redirects_to_login(response, next_url=None):
    """
    Assert response redirects to login page.

    Args:
        response: Django response object
        next_url: Expected 'next' parameter in redirect URL
    """
    assert response.status_code == 302
    assert "/login/" in response.url
    if next_url:
        assert next_url in response.url


def assert_form_has_errors(response, *field_names):
    """
    Assert form in response has errors for specified fields.

    Args:
        response: Django response object
        *field_names: Field names that should have errors
    """
    assert response.status_code == 200
    assert "form" in response.context
    form = response.context["form"]
    assert not form.is_valid()
    for field_name in field_names:
        assert field_name in form.errors, f"Expected error for field '{field_name}'"


def assert_context_contains(response, *keys):
    """
    Assert response context contains specified keys.

    Args:
        response: Django response object
        *keys: Keys that should be in context
    """
    assert response.status_code == 200
    for key in keys:
        assert key in response.context, f"Expected '{key}' in context"


def assert_message_in_response(response, message_text):
    """
    Assert Django message is in response.

    Args:
        response: Django response object
        message_text: Text to search for in messages
    """
    messages = list(response.context.get("messages", []))
    message_strings = [str(m) for m in messages]
    assert any(
        message_text in msg for msg in message_strings
    ), f"Expected message containing '{message_text}' not found"


# ============================================================================
# Database Helpers
# ============================================================================


def count_objects(model_class):
    """
    Count total objects for a model.

    Args:
        model_class: Django model class

    Returns:
        Integer count
    """
    return model_class.objects.count()


def assert_object_exists(model_class, **filters):
    """
    Assert an object exists matching the filters.

    Args:
        model_class: Django model class
        **filters: Lookup filters
    """
    assert model_class.objects.filter(
        **filters
    ).exists(), f"Expected {model_class.__name__} matching {filters} to exist"


def assert_object_not_exists(model_class, **filters):
    """
    Assert no object exists matching the filters.

    Args:
        model_class: Django model class
        **filters: Lookup filters
    """
    assert not model_class.objects.filter(
        **filters
    ).exists(), f"Expected no {model_class.__name__} matching {filters}"


# ============================================================================
# Test Scenario Builders
# ============================================================================


def create_user_with_profile(username="testuser", **profile_data):
    """
    Create a user with profile.

    Args:
        username: Username for the user
        **profile_data: Additional profile data

    Returns:
        Tuple of (user, profile)
    """
    from dogs.models import UserProfile

    user = User.objects.create_user(
        username=username, email=f"{username}@example.com", password="testpass123"
    )

    profile = UserProfile.objects.create(user=user, **profile_data)

    return user, profile


def create_complete_match_scenario():
    """
    Create a complete matching scenario with two users and their dogs.

    Returns:
        Dictionary with users, dogs, and match
    """
    # User 1 with dog
    user1 = User.objects.create_user(
        username="user1", email="user1@example.com", password="pass123"
    )
    dog1 = Dog.objects.create(
        owner=user1,
        name="Dog1",
        breed="Breed1",
        age=3,
        gender="M",
        size="M",
        temperament="friendly",
        looking_for="playmate",
        description="First dog",
    )

    # User 2 with dog
    user2 = User.objects.create_user(
        username="user2", email="user2@example.com", password="pass123"
    )
    dog2 = Dog.objects.create(
        owner=user2,
        name="Dog2",
        breed="Breed2",
        age=4,
        gender="F",
        size="L",
        temperament="playful",
        looking_for="companion",
        description="Second dog",
    )

    # Create match
    match = Match.objects.create(dog_from=dog1, dog_to=dog2, status="pending")

    return {"user1": user1, "user2": user2, "dog1": dog1, "dog2": dog2, "match": match}


def create_bulk_dogs(owner, count=10, **defaults):
    """
    Create multiple dogs for an owner.

    Args:
        owner: User who owns the dogs
        count: Number of dogs to create
        **defaults: Default values for dogs

    Returns:
        List of created dogs
    """
    dogs = []
    for i in range(count):
        dog_data = {
            "name": f"Dog{i}",
            "breed": f"Breed{i}",
            "age": (i % 20) + 1,
            "gender": "M" if i % 2 == 0 else "F",
            "size": ["S", "M", "L"][i % 3],
            "temperament": "friendly",
            "looking_for": "playmate",
            "description": f"Dog number {i}",
        }
        dog_data.update(defaults)
        dog = Dog.objects.create(owner=owner, **dog_data)
        dogs.append(dog)
    return dogs


# ============================================================================
# Cleanup Helpers
# ============================================================================


def cleanup_media_files():
    """Clean up media files created during tests."""
    import os
    import shutil
    from django.conf import settings

    media_root = settings.MEDIA_ROOT
    if os.path.exists(media_root) and "test" in str(media_root).lower():
        shutil.rmtree(media_root, ignore_errors=True)


# ============================================================================
# Comparison Helpers
# ============================================================================


def assert_lists_equal_unordered(list1: List, list2: List):
    """
    Assert two lists contain the same elements (order doesn't matter).

    Args:
        list1: First list
        list2: Second list
    """
    assert sorted(list1) == sorted(
        list2
    ), f"Lists don't match:\nExpected: {sorted(list2)}\nGot: {sorted(list1)}"


def assert_queryset_equal_unordered(qs1, qs2):
    """
    Assert two querysets contain the same objects (order doesn't matter).

    Args:
        qs1: First queryset
        qs2: Second queryset
    """
    list1 = sorted(qs1.values_list("id", flat=True))
    list2 = sorted(qs2.values_list("id", flat=True))
    assert (
        list1 == list2
    ), f"Querysets don't match:\nExpected IDs: {list2}\nGot IDs: {list1}"


# ============================================================================
# URL Helpers
# ============================================================================


def get_url_with_query(url_name, query_params=None, **kwargs):
    """
    Get URL with query parameters.

    Args:
        url_name: Django URL name
        query_params: Dictionary of query parameters
        **kwargs: URL kwargs

    Returns:
        URL string with query parameters
    """
    from django.urls import reverse
    from urllib.parse import urlencode

    url = reverse(url_name, kwargs=kwargs)
    if query_params:
        url += "?" + urlencode(query_params)
    return url


# ============================================================================
# Mock Helpers
# ============================================================================


def create_mock_request(user=None, method="GET", data=None):
    """
    Create a mock request object for testing.

    Args:
        user: User to attach to request
        method: HTTP method
        data: Request data

    Returns:
        Mock request object
    """
    from django.test import RequestFactory
    from django.contrib.auth.models import AnonymousUser

    factory = RequestFactory()
    request = getattr(factory, method.lower())("/", data=data or {})
    request.user = user if user else AnonymousUser()
    return request


# ============================================================================
# Time Helpers
# ============================================================================


def freeze_time(datetime_obj):
    """
    Context manager to freeze time for testing.

    Args:
        datetime_obj: Datetime to freeze at

    Returns:
        Context manager
    """
    try:
        from freezegun import freeze_time as fg_freeze_time

        return fg_freeze_time(datetime_obj)
    except ImportError:
        # If freezegun not installed, return a no-op context manager
        from contextlib import contextmanager

        @contextmanager
        def noop():
            yield

        return noop()
