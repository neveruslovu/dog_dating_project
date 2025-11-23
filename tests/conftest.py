"""
Pytest Configuration and Shared Fixtures for DogDating Tests

This module provides reusable test fixtures for all test modules.
It follows pytest best practices for fixture design and scoping.
"""

import os
import sys
import django
from django.conf import settings

# Ensure Django settings are configured before importing models
if not settings.configured:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.test")
    django.setup()

import pytest
from django.contrib.auth.models import User, AnonymousUser
from django.test import Client
from dogs.models import Dog, UserProfile, Match, Favorite, Message
from menu_app.models import Menu, MenuItem


# ============================================================================
# User Fixtures
# ============================================================================


@pytest.fixture
def user(db):
    """Create a regular authenticated user."""
    return User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def user2(db):
    """Create a second user for relationship tests."""
    return User.objects.create_user(
        username="testuser2",
        email="testuser2@example.com",
        password="testpass123",
        first_name="Test2",
        last_name="User2",
    )


@pytest.fixture
def user3(db):
    """Create a third user for complex scenarios."""
    return User.objects.create_user(
        username="testuser3", email="testuser3@example.com", password="testpass123"
    )


@pytest.fixture
def staff_user(db):
    """Create a staff user for admin tests."""
    return User.objects.create_user(
        username="staffuser",
        email="staff@example.com",
        password="staffpass123",
        is_staff=True,
    )


@pytest.fixture
def superuser(db):
    """Create a superuser for admin tests."""
    return User.objects.create_superuser(
        username="admin", email="admin@example.com", password="adminpass123"
    )


@pytest.fixture
def anonymous_user():
    """Create an anonymous user."""
    return AnonymousUser()


# ============================================================================
# Client Fixtures
# ============================================================================


@pytest.fixture
def client():
    """Django test client."""
    return Client()


@pytest.fixture
def authenticated_client(client, user):
    """Client logged in as regular user."""
    client.force_login(user)
    return client


@pytest.fixture
def staff_client(client, staff_user):
    """Client logged in as staff user."""
    client.force_login(staff_user)
    return client


@pytest.fixture
def admin_client(client, superuser):
    """Client logged in as superuser."""
    client.force_login(superuser)
    return client


# ============================================================================
# UserProfile Fixtures
# ============================================================================


@pytest.fixture
def user_profile(db, user):
    """Create a user profile."""
    return UserProfile.objects.create(
        user=user,
        bio="Test bio for testuser",
        location="Test City",
        phone="+1234567890",
    )


@pytest.fixture
def user2_profile(db, user2):
    """Create a profile for user2."""
    return UserProfile.objects.create(
        user=user2,
        bio="Test bio for testuser2",
        location="Another City",
        phone="+0987654321",
    )


# ============================================================================
# Dog Fixtures
# ============================================================================


@pytest.fixture
def dog(db, user):
    """Create a dog owned by user."""
    return Dog.objects.create(
        owner=user,
        name="Buddy",
        breed="Golden Retriever",
        age=3,
        gender="M",
        size="L",
        temperament="friendly and energetic",
        looking_for="playmate",
        description="A friendly golden retriever who loves to play fetch.",
    )


@pytest.fixture
def dog2(db, user):
    """Create a second dog owned by user."""
    return Dog.objects.create(
        owner=user,
        name="Max",
        breed="German Shepherd",
        age=5,
        gender="M",
        size="L",
        temperament="loyal and protective",
        looking_for="companion",
        description="A loyal companion and protector.",
    )


@pytest.fixture
def other_dog(db, user2):
    """Create a dog owned by user2."""
    return Dog.objects.create(
        owner=user2,
        name="Luna",
        breed="Labrador",
        age=2,
        gender="F",
        size="M",
        temperament="playful and gentle",
        looking_for="friendship",
        description="A gentle and playful lab who loves everyone.",
    )


@pytest.fixture
def inactive_dog(db, user):
    """Create an inactive dog."""
    return Dog.objects.create(
        owner=user,
        name="Retired",
        breed="Senior Dog",
        age=15,
        gender="M",
        size="M",
        temperament="calm",
        looking_for="companion",
        description="A retired senior dog.",
        is_active=False,
    )


@pytest.fixture
def multiple_dogs(db, user, user2):
    """Create multiple dogs for pagination tests."""
    dogs = []
    for i in range(15):
        owner = user if i % 2 == 0 else user2
        dogs.append(
            Dog.objects.create(
                owner=owner,
                name=f"Dog{i}",
                breed=f"Breed{i}",
                age=(i % 20) + 1,
                gender="M" if i % 2 == 0 else "F",
                size=["S", "M", "L"][i % 3],
                temperament="friendly",
                looking_for="playmate",
                description=f"Dog number {i}",
            )
        )
    return dogs


# ============================================================================
# Match Fixtures
# ============================================================================


@pytest.fixture
def pending_match(db, dog, other_dog):
    """Create a pending match."""
    return Match.objects.create(dog_from=dog, dog_to=other_dog, status="pending")


@pytest.fixture
def accepted_match(db, dog, other_dog):
    """Create an accepted match."""
    return Match.objects.create(dog_from=dog, dog_to=other_dog, status="accepted")


@pytest.fixture
def declined_match(db, dog, other_dog):
    """Create a declined match."""
    return Match.objects.create(dog_from=dog, dog_to=other_dog, status="declined")


@pytest.fixture
def multiple_matches(db, dog, dog2, other_dog, user3):
    """Create multiple matches for testing."""
    dog3 = Dog.objects.create(
        owner=user3,
        name="Charlie",
        breed="Beagle",
        age=4,
        gender="M",
        size="M",
        temperament="curious",
        looking_for="playmate",
        description="Curious beagle",
    )

    return [
        Match.objects.create(dog_from=dog, dog_to=other_dog, status="pending"),
        Match.objects.create(dog_from=dog, dog_to=dog3, status="accepted"),
        Match.objects.create(dog_from=dog2, dog_to=other_dog, status="declined"),
        Match.objects.create(dog_from=other_dog, dog_to=dog, status="pending"),
    ]


# ============================================================================
# Favorite Fixtures
# ============================================================================


@pytest.fixture
def favorite(db, user, other_dog):
    """Create a favorite."""
    return Favorite.objects.create(user=user, dog=other_dog)


@pytest.fixture
def multiple_favorites(db, user, multiple_dogs):
    """Create multiple favorites for pagination tests."""
    favorites = []
    for dog in multiple_dogs[:12]:
        if dog.owner != user:  # Can't favorite own dogs
            favorites.append(Favorite.objects.create(user=user, dog=dog))
    return favorites


# ============================================================================
# Message Fixtures
# ============================================================================


@pytest.fixture
def message(db, user, user2):
    """Create a message from user to user2."""
    return Message.objects.create(
        sender=user,
        receiver=user2,
        subject="Test Subject",
        content="Test message content",
        is_read=False,
    )


@pytest.fixture
def read_message(db, user, user2):
    """Create a read message."""
    return Message.objects.create(
        sender=user,
        receiver=user2,
        subject="Read Message",
        content="This message has been read",
        is_read=True,
    )


# ============================================================================
# Menu Fixtures
# ============================================================================


@pytest.fixture
def menu(db):
    """Create a menu."""
    return Menu.objects.create(name="Main Menu", description="Main navigation menu")


@pytest.fixture
def menu_item(db, menu):
    """Create a menu item."""
    return MenuItem.objects.create(menu=menu, title="Home", url="/", order=1)


@pytest.fixture
def guest_menu(db):
    """Create a guest menu with items."""
    menu = Menu.objects.create(
        name="Guest Menu", description="Menu for unauthenticated users"
    )

    items = [
        MenuItem.objects.create(menu=menu, title="О сервисе", url="/about/", order=1),
        MenuItem.objects.create(menu=menu, title="Вход", url="/login/", order=2),
        MenuItem.objects.create(
            menu=menu, title="Регистрация", url="/register/", order=3
        ),
    ]

    return menu, items


# ============================================================================
# Form Data Fixtures
# ============================================================================


@pytest.fixture
def valid_dog_data():
    """Valid data for creating a dog."""
    return {
        "name": "TestDog",
        "breed": "Test Breed",
        "age": 3,
        "gender": "M",
        "size": "M",
        "temperament": "friendly",
        "looking_for": "playmate",
        "description": "A test dog for testing purposes",
    }


@pytest.fixture
def valid_user_data():
    """Valid data for user registration."""
    return {
        "username": "newuser",
        "email": "newuser@example.com",
        "password1": "testpass123!",
        "password2": "testpass123!",
    }


@pytest.fixture
def valid_login_data():
    """Valid login credentials."""
    return {"username": "testuser", "password": "testpass123"}


@pytest.fixture
def valid_profile_data():
    """Valid data for profile update."""
    return {"bio": "Updated bio", "location": "Updated City", "phone": "+1111111111"}


# ============================================================================
# Helper Fixtures
# ============================================================================


@pytest.fixture
def create_dog():
    """Factory function to create dogs on demand."""

    def _create_dog(owner, **kwargs):
        defaults = {
            "name": "TestDog",
            "breed": "Test Breed",
            "age": 3,
            "gender": "M",
            "size": "M",
            "temperament": "friendly",
            "looking_for": "playmate",
            "description": "Test dog",
        }
        defaults.update(kwargs)
        return Dog.objects.create(owner=owner, **defaults)

    return _create_dog


@pytest.fixture
def create_match():
    """Factory function to create matches on demand."""

    def _create_match(dog_from, dog_to, status="pending"):
        return Match.objects.create(dog_from=dog_from, dog_to=dog_to, status=status)

    return _create_match


@pytest.fixture
def create_favorite():
    """Factory function to create favorites on demand."""

    def _create_favorite(user, dog):
        return Favorite.objects.create(user=user, dog=dog)

    return _create_favorite


# ============================================================================
# Database Marker
# ============================================================================


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Automatically enable database access for all tests.
    Can be overridden by specific test functions if needed.
    """
    pass
