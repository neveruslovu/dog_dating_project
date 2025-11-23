"""
Comprehensive Dog Model Tests

Tests all aspects of the Dog model including:
- CRUD operations
- Field validations
- Unique constraints
- Relationships
- Custom methods
- Edge cases
"""

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from dogs.models import Dog, Favorite, Match


@pytest.mark.models
@pytest.mark.unit
class TestDogModel:
    """Test suite for Dog model basic operations."""

    def test_dog_creation_with_all_fields(self, user):
        """Test creating a dog with all required and optional fields."""
        dog = Dog.objects.create(
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

        assert dog.id is not None
        assert dog.owner == user
        assert dog.name == "Buddy"
        assert dog.breed == "Golden Retriever"
        assert dog.age == 3
        assert dog.gender == "M"
        assert dog.size == "L"
        assert dog.temperament == "friendly and energetic"
        assert dog.looking_for == "playmate"
        assert dog.description == "A friendly golden retriever who loves to play fetch."
        assert dog.is_active is True
        assert dog.created_at is not None
        assert dog.updated_at is not None

    def test_dog_str_representation(self, dog):
        """Test __str__ method includes name and owner username."""
        expected = f"{dog.name} ({dog.owner.username})"
        assert str(dog) == expected

    def test_dog_update(self, dog):
        """Test updating dog fields."""
        dog.age = 4
        dog.temperament = "calm and relaxed"
        dog.save()

        updated_dog = Dog.objects.get(id=dog.id)
        assert updated_dog.age == 4
        assert updated_dog.temperament == "calm and relaxed"

    def test_dog_deletion(self, dog):
        """Test deleting a dog."""
        dog_id = dog.id
        dog.delete()

        with pytest.raises(Dog.DoesNotExist):
            Dog.objects.get(id=dog_id)

    def test_dog_is_active_default_true(self, user):
        """Test that is_active defaults to True."""
        dog = Dog.objects.create(
            owner=user,
            name="Test",
            breed="Test",
            age=2,
            gender="M",
            size="M",
            temperament="friendly",
            looking_for="playmate",
            description="Test",
        )
        assert dog.is_active is True

    def test_dog_can_be_inactive(self, user):
        """Test setting dog as inactive."""
        dog = Dog.objects.create(
            owner=user,
            name="Retired",
            breed="Senior",
            age=15,
            gender="M",
            size="M",
            temperament="calm",
            looking_for="companion",
            description="Retired dog",
            is_active=False,
        )
        assert dog.is_active is False


@pytest.mark.models
@pytest.mark.unit
class TestDogValidations:
    """Test Dog model field validations."""

    def test_dog_age_minimum_zero(self, user, valid_dog_data):
        """Test that age 0 is valid (newborn)."""
        dog = Dog.objects.create(
            owner=user, age=0, **{k: v for k, v in valid_dog_data.items() if k != "age"}
        )
        dog.full_clean()  # Should not raise ValidationError
        assert dog.age == 0

    def test_dog_age_maximum_twenty(self, user, valid_dog_data):
        """Test that age 20 is valid."""
        dog = Dog.objects.create(
            owner=user,
            age=20,
            **{k: v for k, v in valid_dog_data.items() if k != "age"},
        )
        dog.full_clean()  # Should not raise ValidationError
        assert dog.age == 20

    def test_dog_age_exceeds_maximum(self, user, valid_dog_data):
        """Test that age > 20 raises ValidationError."""
        dog = Dog.objects.create(
            owner=user,
            age=21,
            **{k: v for k, v in valid_dog_data.items() if k != "age"},
        )
        with pytest.raises(ValidationError):
            dog.full_clean()

    def test_dog_age_negative_raises_error(self, user, valid_dog_data):
        """Test that negative age raises IntegrityError in Django 5.x."""
        from django.db import IntegrityError

        with pytest.raises(IntegrityError):
            Dog.objects.create(
                owner=user,
                age=-1,
                **{k: v for k, v in valid_dog_data.items() if k != "age"},
            )

    def test_dog_name_required(self, user):
        """Test that name field is required."""
        from django.core.exceptions import ValidationError
        from django.db import IntegrityError as DBIntegrityError

        # In Django 5.x, trying to save with empty required CharField raises ValidationError
        with pytest.raises(
            (IntegrityError, DBIntegrityError, ValidationError, TypeError)
        ):
            dog = Dog(
                owner=user,
                breed="Test",
                age=3,
                gender="M",
                size="M",
                temperament="friendly",
                looking_for="playmate",
                description="Test",
                # Missing name - will be None
            )
            dog.full_clean()  # This will raise ValidationError
            dog.save()  # This might raise IntegrityError

    def test_dog_breed_required(self, user):
        """Test that breed field is required."""
        from django.core.exceptions import ValidationError
        from django.db import IntegrityError as DBIntegrityError

        # In Django 5.x, trying to save with empty required CharField raises ValidationError
        with pytest.raises(
            (IntegrityError, DBIntegrityError, ValidationError, TypeError)
        ):
            dog = Dog(
                owner=user,
                name="Test",
                age=3,
                gender="M",
                size="M",
                temperament="friendly",
                looking_for="playmate",
                description="Test",
                # Missing breed - will be None
            )
            dog.full_clean()  # This will raise ValidationError
            dog.save()  # This might raise IntegrityError

    def test_dog_gender_choices(self, user, valid_dog_data):
        """Test gender field accepts only M or F."""
        # Valid: M
        dog_m = Dog.objects.create(
            owner=user,
            gender="M",
            **{k: v for k, v in valid_dog_data.items() if k != "gender"},
        )
        assert dog_m.gender == "M"

        # Valid: F
        dog_f = Dog.objects.create(
            owner=user,
            name="Luna",
            gender="F",
            **{k: v for k, v in valid_dog_data.items() if k not in ["gender", "name"]},
        )
        assert dog_f.gender == "F"

    def test_dog_size_choices(self, user, valid_dog_data):
        """Test size field accepts S, M, or L."""
        for size in ["S", "M", "L"]:
            dog = Dog.objects.create(
                owner=user,
                name=f"Dog{size}",
                size=size,
                **{
                    k: v for k, v in valid_dog_data.items() if k not in ["size", "name"]
                },
            )
            assert dog.size == size

    def test_dog_looking_for_choices(self, user, valid_dog_data):
        """Test looking_for field accepts valid choices."""
        choices = ["playmate", "companion", "mate", "friendship"]
        for choice in choices:
            dog = Dog.objects.create(
                owner=user,
                name=f"Dog{choice}",
                looking_for=choice,
                **{
                    k: v
                    for k, v in valid_dog_data.items()
                    if k not in ["looking_for", "name"]
                },
            )
            assert dog.looking_for == choice


@pytest.mark.models
@pytest.mark.unit
class TestDogUniqueConstraints:
    """Test Dog model unique constraints."""

    def test_dog_name_unique_per_owner(self, user):
        """Test that a user cannot create two dogs with the same name."""
        Dog.objects.create(
            owner=user,
            name="Buddy",
            breed="Breed1",
            age=3,
            gender="M",
            size="M",
            temperament="friendly",
            looking_for="playmate",
            description="First Buddy",
        )

        # Try creating another dog with the same name and owner
        dog2 = Dog(
            owner=user,
            name="Buddy",
            breed="Breed2",
            age=5,
            gender="F",
            size="L",
            temperament="calm",
            looking_for="companion",
            description="Second Buddy",
        )

        with pytest.raises(ValidationError):
            dog2.full_clean()

    def test_different_users_can_have_same_dog_name(self, user, user2):
        """Test that different users can have dogs with the same name."""
        dog1 = Dog.objects.create(
            owner=user,
            name="Buddy",
            breed="Breed1",
            age=3,
            gender="M",
            size="M",
            temperament="friendly",
            looking_for="playmate",
            description="User1's Buddy",
        )

        dog2 = Dog.objects.create(
            owner=user2,
            name="Buddy",
            breed="Breed2",
            age=4,
            gender="F",
            size="L",
            temperament="calm",
            looking_for="companion",
            description="User2's Buddy",
        )

        assert dog1.name == dog2.name
        assert dog1.owner != dog2.owner
        assert dog1.id != dog2.id


@pytest.mark.models
@pytest.mark.unit
class TestDogRelationships:
    """Test Dog model relationships with other models."""

    def test_dog_owner_relationship(self, dog, user):
        """Test Dog belongs to User via owner field."""
        assert dog.owner == user
        assert dog in user.dogs.all()

    def test_dog_cascade_deletion_with_owner(self, user):
        """Test that deleting owner cascades to their dogs."""
        dog = Dog.objects.create(
            owner=user,
            name="Buddy",
            breed="Test",
            age=3,
            gender="M",
            size="M",
            temperament="friendly",
            looking_for="playmate",
            description="Test dog",
        )
        dog_id = dog.id

        user.delete()

        with pytest.raises(Dog.DoesNotExist):
            Dog.objects.get(id=dog_id)

    def test_dog_favorites_relationship(self, dog, user2):
        """Test Dog can be favorited by users."""
        favorite = Favorite.objects.create(user=user2, dog=dog)

        assert favorite in dog.favorited_by.all()
        # In Django 5.x, use the related manager more explicitly
        favorite_dogs = [f.dog for f in user2.favorite_dogs.all()]
        assert dog in favorite_dogs

    def test_dog_matches_sent_relationship(self, dog, other_dog):
        """Test Dog can send match requests."""
        match = Match.objects.create(dog_from=dog, dog_to=other_dog, status="pending")

        assert match in dog.matches_sent.all()

    def test_dog_matches_received_relationship(self, dog, other_dog):
        """Test Dog can receive match requests."""
        match = Match.objects.create(dog_from=other_dog, dog_to=dog, status="pending")

        assert match in dog.matches_received.all()


@pytest.mark.models
@pytest.mark.unit
class TestDogHasPhotoProperty:
    """Test Dog.has_photo property."""

    def test_has_photo_false_when_no_photo(self, dog):
        """Test has_photo returns False when no photo attached."""
        # In Django 5.x, check using bool() or truthiness
        assert not dog.photo
        assert dog.has_photo is False

    def test_has_photo_returns_correct_value(self, dog):
        """Test has_photo accurately reflects photo presence."""
        # Initially no photo
        assert dog.has_photo is False

        # Note: Actually testing with real file uploads requires more setup
        # This tests the property logic when photo field is empty


@pytest.mark.models
@pytest.mark.unit
class TestDogQuerysets:
    """Test Dog model querysets and filtering."""

    def test_filter_active_dogs(self, user):
        """Test filtering active dogs."""
        active_dog = Dog.objects.create(
            owner=user,
            name="Active",
            breed="Breed",
            age=3,
            gender="M",
            size="M",
            temperament="friendly",
            looking_for="playmate",
            description="Active",
            is_active=True,
        )
        inactive_dog = Dog.objects.create(
            owner=user,
            name="Inactive",
            breed="Breed",
            age=3,
            gender="M",
            size="M",
            temperament="friendly",
            looking_for="playmate",
            description="Inactive",
            is_active=False,
        )

        active_dogs = Dog.objects.filter(is_active=True)
        assert active_dog in active_dogs
        assert inactive_dog not in active_dogs

    def test_filter_by_breed(self, multiple_dogs):
        """Test filtering dogs by breed."""
        # multiple_dogs fixture creates 15 dogs with different breeds
        breed_dogs = Dog.objects.filter(breed="Breed5")
        assert breed_dogs.count() >= 1

    def test_filter_by_age_range(self, multiple_dogs):
        """Test filtering dogs by age range."""
        young_dogs = Dog.objects.filter(age__gte=0, age__lte=3)
        assert young_dogs.count() > 0

    def test_filter_by_gender(self, multiple_dogs):
        """Test filtering dogs by gender."""
        male_dogs = Dog.objects.filter(gender="M")
        female_dogs = Dog.objects.filter(gender="F")

        assert male_dogs.count() > 0
        assert female_dogs.count() > 0

    def test_filter_by_size(self, multiple_dogs):
        """Test filtering dogs by size."""
        for size in ["S", "M", "L"]:
            size_dogs = Dog.objects.filter(size=size)
            assert size_dogs.count() > 0

    def test_order_by_created_at(self, multiple_dogs):
        """Test default ordering by -created_at."""
        dogs = Dog.objects.all()
        # Default ordering should be by -created_at (newest first)
        assert dogs[0].created_at >= dogs[len(dogs) - 1].created_at


@pytest.mark.models
@pytest.mark.unit
class TestDogEdgeCases:
    """Test Dog model edge cases and boundary values."""

    def test_dog_with_long_description(self, user, valid_dog_data):
        """Test dog with maximum length description."""
        long_description = "A" * 5000
        dog = Dog.objects.create(
            owner=user,
            description=long_description,
            **{k: v for k, v in valid_dog_data.items() if k != "description"},
        )
        assert dog.description == long_description

    def test_dog_with_empty_temperament(self, user, valid_dog_data):
        """Test that temperament can be empty string."""
        dog = Dog.objects.create(
            owner=user,
            temperament="",
            **{k: v for k, v in valid_dog_data.items() if k != "temperament"},
        )
        assert dog.temperament == ""

    def test_dog_with_special_characters_in_name(self, user, valid_dog_data):
        """Test dog name can contain special characters."""
        special_names = ["Buddy-Max", "Luna's Dog", "Rex (Junior)", "Fido #1"]

        for name in special_names:
            dog = Dog.objects.create(
                owner=user,
                name=name,
                **{k: v for k, v in valid_dog_data.items() if k != "name"},
            )
            assert dog.name == name
            dog.delete()  # Clean up for next iteration

    def test_dog_with_unicode_in_breed(self, user, valid_dog_data):
        """Test breed can contain unicode characters."""
        dog = Dog.objects.create(
            owner=user,
            breed="Немецкая овчарка",  # German Shepherd in Russian
            **{k: v for k, v in valid_dog_data.items() if k != "breed"},
        )
        assert dog.breed == "Немецкая овчарка"
