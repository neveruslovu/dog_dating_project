"""
Factory Boy factories for generating test data

This module provides factory classes for creating test objects with realistic data.
Uses factory_boy and Faker for generating test data efficiently.

Usage:
    from tests.factories import UserFactory, DogFactory

    user = UserFactory()
    dog = DogFactory(owner=user)
    dogs = DogFactory.create_batch(10)
"""

import factory
from factory.django import DjangoModelFactory
from factory import fuzzy
from django.contrib.auth.models import User
from dogs.models import Dog, UserProfile, Match, Favorite, Message
from menu_app.models import Menu, MenuItem
import random


# ============================================================================
# User Factories
# ============================================================================


class UserFactory(DjangoModelFactory):
    """Factory for creating User instances."""

    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True
    is_staff = False
    is_superuser = False

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        """Set password after user creation."""
        if not create:
            return

        if extracted:
            self.set_password(extracted)
        else:
            self.set_password("testpass123")


class StaffUserFactory(UserFactory):
    """Factory for creating staff users."""

    is_staff = True


class SuperUserFactory(UserFactory):
    """Factory for creating superusers."""

    is_staff = True
    is_superuser = True


# ============================================================================
# UserProfile Factories
# ============================================================================


class UserProfileFactory(DjangoModelFactory):
    """Factory for creating UserProfile instances."""

    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    bio = factory.Faker("text", max_nb_chars=200)
    location = factory.Faker("city")
    phone = factory.Faker("phone_number")


# ============================================================================
# Dog Factories
# ============================================================================


class DogFactory(DjangoModelFactory):
    """Factory for creating Dog instances."""

    class Meta:
        model = Dog

    owner = factory.SubFactory(UserFactory)
    name = factory.Faker("first_name")
    breed = factory.Faker(
        "random_element",
        elements=[
            "Golden Retriever",
            "Labrador",
            "German Shepherd",
            "Beagle",
            "Poodle",
            "Bulldog",
            "Rottweiler",
            "Yorkshire Terrier",
            "Boxer",
            "Dachshund",
            "Siberian Husky",
            "Pomeranian",
        ],
    )
    age = fuzzy.FuzzyInteger(0, 20)
    gender = fuzzy.FuzzyChoice(["M", "F"])
    size = fuzzy.FuzzyChoice(["S", "M", "L"])
    temperament = factory.Faker(
        "random_element",
        elements=[
            "friendly",
            "energetic",
            "calm",
            "playful",
            "loyal",
            "protective",
            "gentle",
            "curious",
            "independent",
            "social",
        ],
    )
    looking_for = fuzzy.FuzzyChoice(["playmate", "companion", "mate", "friendship"])
    description = factory.Faker("text", max_nb_chars=300)
    is_active = True

    @factory.lazy_attribute
    def name(self):
        """Generate unique dog names."""
        dog_names = [
            "Buddy",
            "Max",
            "Charlie",
            "Lucy",
            "Luna",
            "Cooper",
            "Daisy",
            "Milo",
            "Bella",
            "Bailey",
            "Rocky",
            "Molly",
            "Duke",
            "Sadie",
            "Jack",
            "Maggie",
            "Bear",
            "Sophie",
            "Zeus",
            "Lola",
            "Tucker",
            "Stella",
            "Oliver",
            "Chloe",
        ]
        return random.choice(dog_names)


class InactiveDogFactory(DogFactory):
    """Factory for creating inactive dogs."""

    is_active = False


class PuppyFactory(DogFactory):
    """Factory for creating puppies (0-1 years old)."""

    age = fuzzy.FuzzyInteger(0, 1)
    temperament = "playful and energetic"


class SeniorDogFactory(DogFactory):
    """Factory for creating senior dogs (10+ years old)."""

    age = fuzzy.FuzzyInteger(10, 20)
    temperament = "calm and gentle"


# ============================================================================
# Match Factories
# ============================================================================


class MatchFactory(DjangoModelFactory):
    """Factory for creating Match instances."""

    class Meta:
        model = Match

    dog_from = factory.SubFactory(DogFactory)
    dog_to = factory.SubFactory(DogFactory)
    status = "pending"


class PendingMatchFactory(MatchFactory):
    """Factory for pending matches."""

    status = "pending"


class AcceptedMatchFactory(MatchFactory):
    """Factory for accepted matches."""

    status = "accepted"


class DeclinedMatchFactory(MatchFactory):
    """Factory for declined matches."""

    status = "declined"


# ============================================================================
# Favorite Factories
# ============================================================================


class FavoriteFactory(DjangoModelFactory):
    """Factory for creating Favorite instances."""

    class Meta:
        model = Favorite

    user = factory.SubFactory(UserFactory)
    dog = factory.SubFactory(DogFactory)


# ============================================================================
# Message Factories
# ============================================================================


class MessageFactory(DjangoModelFactory):
    """Factory for creating Message instances."""

    class Meta:
        model = Message

    sender = factory.SubFactory(UserFactory)
    receiver = factory.SubFactory(UserFactory)
    subject = factory.Faker("sentence", nb_words=6)
    content = factory.Faker("text", max_nb_chars=500)
    is_read = False


class ReadMessageFactory(MessageFactory):
    """Factory for read messages."""

    is_read = True


# ============================================================================
# Menu Factories
# ============================================================================


class MenuFactory(DjangoModelFactory):
    """Factory for creating Menu instances."""

    class Meta:
        model = Menu

    name = factory.Sequence(lambda n: f"Menu {n}")
    description = factory.Faker("sentence")


class MenuItemFactory(DjangoModelFactory):
    """Factory for creating MenuItem instances."""

    class Meta:
        model = MenuItem

    menu = factory.SubFactory(MenuFactory)
    title = factory.Faker("word")
    url = factory.Faker("uri_path")
    order = factory.Sequence(lambda n: n)


# ============================================================================
# Utility Functions
# ============================================================================


def create_user_with_dogs(num_dogs=3):
    """
    Create a user with multiple dogs.

    Args:
        num_dogs: Number of dogs to create

    Returns:
        Tuple of (user, list_of_dogs)
    """
    user = UserFactory()
    dogs = DogFactory.create_batch(num_dogs, owner=user)
    return user, dogs


def create_match_scenario():
    """
    Create a complete match scenario with two users and their dogs.

    Returns:
        Dict with users, dogs, and match
    """
    user1, dogs1 = create_user_with_dogs(2)
    user2, dogs2 = create_user_with_dogs(2)

    match = MatchFactory(dog_from=dogs1[0], dog_to=dogs2[0], status="pending")

    return {
        "user1": user1,
        "user2": user2,
        "dogs1": dogs1,
        "dogs2": dogs2,
        "match": match,
    }


def create_favorites_scenario(user, num_favorites=5):
    """
    Create a user with multiple favorites.

    Args:
        user: User instance
        num_favorites: Number of favorites to create

    Returns:
        List of favorite instances
    """
    # Create dogs owned by other users
    other_dogs = []
    for _ in range(num_favorites):
        other_user = UserFactory()
        dog = DogFactory(owner=other_user)
        other_dogs.append(dog)

    # Create favorites
    favorites = []
    for dog in other_dogs:
        favorite = FavoriteFactory(user=user, dog=dog)
        favorites.append(favorite)

    return favorites


def create_complete_user():
    """
    Create a complete user with profile, dogs, matches, and favorites.

    Returns:
        Dict with all related objects
    """
    user = UserFactory()
    profile = UserProfileFactory(user=user)
    dogs = DogFactory.create_batch(3, owner=user)

    # Create other users and their dogs for matches/favorites
    other_user1 = UserFactory()
    other_dogs1 = DogFactory.create_batch(2, owner=other_user1)

    other_user2 = UserFactory()
    other_dogs2 = DogFactory.create_batch(2, owner=other_user2)

    # Create matches
    matches = [
        MatchFactory(dog_from=dogs[0], dog_to=other_dogs1[0], status="pending"),
        MatchFactory(dog_from=dogs[1], dog_to=other_dogs2[0], status="accepted"),
    ]

    # Create favorites
    favorites = [
        FavoriteFactory(user=user, dog=other_dogs1[1]),
        FavoriteFactory(user=user, dog=other_dogs2[1]),
    ]

    return {
        "user": user,
        "profile": profile,
        "dogs": dogs,
        "matches": matches,
        "favorites": favorites,
        "other_users": [other_user1, other_user2],
        "other_dogs": other_dogs1 + other_dogs2,
    }


# ============================================================================
# Batch Creation Helpers
# ============================================================================


def create_multiple_users_with_dogs(num_users=5, dogs_per_user=2):
    """
    Create multiple users, each with several dogs.

    Args:
        num_users: Number of users to create
        dogs_per_user: Number of dogs per user

    Returns:
        List of dicts with user and their dogs
    """
    result = []
    for _ in range(num_users):
        user, dogs = create_user_with_dogs(dogs_per_user)
        result.append({"user": user, "dogs": dogs})
    return result


def create_pagination_dataset(total_items=50):
    """
    Create a large dataset for pagination testing.

    Args:
        total_items: Number of dogs to create

    Returns:
        List of dog instances
    """
    # Create multiple owners
    owners = UserFactory.create_batch(10)

    # Create dogs distributed among owners
    dogs = []
    for i in range(total_items):
        owner = owners[i % len(owners)]
        dog = DogFactory(owner=owner)
        dogs.append(dog)

    return dogs
