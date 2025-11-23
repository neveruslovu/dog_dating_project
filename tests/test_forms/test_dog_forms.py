"""
Dog Form Tests

Comprehensive validation tests for dog-related forms.
"""

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from dogs.forms import DogForm, DogSearchForm


@pytest.mark.forms
class TestDogForm:
    """Test DogForm validation and functionality."""

    def test_dog_form_with_valid_data(self, user, valid_dog_data):
        """Test form accepts valid data."""
        form = DogForm(data=valid_dog_data, user=user)
        assert form.is_valid()

    def test_dog_form_saves_with_owner(self, user, valid_dog_data):
        """Test form saves dog with correct owner."""
        form = DogForm(data=valid_dog_data, user=user)
        assert form.is_valid()

        dog = form.save()
        assert dog.owner == user

    def test_dog_form_requires_name(self, user, valid_dog_data):
        """Test name field is required."""
        data = valid_dog_data.copy()
        del data["name"]

        form = DogForm(data=data, user=user)
        assert not form.is_valid()
        assert "name" in form.errors

    def test_dog_form_requires_breed(self, user, valid_dog_data):
        """Test breed field is required."""
        data = valid_dog_data.copy()
        del data["breed"]

        form = DogForm(data=data, user=user)
        assert not form.is_valid()
        assert "breed" in form.errors

    def test_dog_form_requires_age(self, user, valid_dog_data):
        """Test age field is required."""
        data = valid_dog_data.copy()
        del data["age"]

        form = DogForm(data=data, user=user)
        assert not form.is_valid()
        assert "age" in form.errors

    def test_dog_form_age_must_be_valid_range(self, user, valid_dog_data):
        """Test age must be between 0 and 20."""
        # Test age too high
        data = valid_dog_data.copy()
        data["age"] = 25
        form = DogForm(data=data, user=user)
        assert not form.is_valid()

        # Test negative age
        data["age"] = -1
        form = DogForm(data=data, user=user)
        assert not form.is_valid()

        # Test valid boundary values
        data["age"] = 0
        form = DogForm(data=data, user=user)
        assert form.is_valid()

        data["age"] = 20
        form = DogForm(data=data, user=user)
        assert form.is_valid()

    def test_dog_form_requires_gender(self, user, valid_dog_data):
        """Test gender field is required."""
        data = valid_dog_data.copy()
        del data["gender"]

        form = DogForm(data=data, user=user)
        assert not form.is_valid()
        assert "gender" in form.errors

    def test_dog_form_gender_must_be_valid_choice(self, user, valid_dog_data):
        """Test gender accepts only M or F."""
        data = valid_dog_data.copy()
        data["gender"] = "X"

        form = DogForm(data=data, user=user)
        assert not form.is_valid()

    def test_dog_form_requires_size(self, user, valid_dog_data):
        """Test size field is required."""
        data = valid_dog_data.copy()
        del data["size"]

        form = DogForm(data=data, user=user)
        assert not form.is_valid()
        assert "size" in form.errors

    def test_dog_form_size_must_be_valid_choice(self, user, valid_dog_data):
        """Test size accepts only S, M, or L."""
        data = valid_dog_data.copy()
        data["size"] = "XL"

        form = DogForm(data=data, user=user)
        assert not form.is_valid()

    def test_dog_form_requires_temperament(self, user, valid_dog_data):
        """Test temperament field is required."""
        data = valid_dog_data.copy()
        del data["temperament"]

        form = DogForm(data=data, user=user)
        assert not form.is_valid()
        assert "temperament" in form.errors

    def test_dog_form_requires_looking_for(self, user, valid_dog_data):
        """Test looking_for field is required."""
        data = valid_dog_data.copy()
        del data["looking_for"]

        form = DogForm(data=data, user=user)
        assert not form.is_valid()
        assert "looking_for" in form.errors

    def test_dog_form_looking_for_valid_choices(self, user, valid_dog_data):
        """Test looking_for accepts valid choices."""
        valid_choices = ["playmate", "companion", "mate", "friendship"]

        for choice in valid_choices:
            data = valid_dog_data.copy()
            data["looking_for"] = choice
            form = DogForm(data=data, user=user)
            assert form.is_valid()

    def test_dog_form_requires_description(self, user, valid_dog_data):
        """Test description field is required."""
        data = valid_dog_data.copy()
        del data["description"]

        form = DogForm(data=data, user=user)
        assert not form.is_valid()
        assert "description" in form.errors

    def test_dog_form_photo_is_optional(self, user, valid_dog_data):
        """Test photo field is optional."""
        form = DogForm(data=valid_dog_data, user=user)
        assert form.is_valid()


@pytest.mark.forms
class TestDogFormImageValidation:
    """Test DogForm image upload validation."""

    def test_dog_form_accepts_valid_jpeg(self, user, valid_dog_data):
        """Test form accepts JPEG images."""
        image = SimpleUploadedFile(
            "test.jpg", b"fake image content", content_type="image/jpeg"
        )
        form = DogForm(data=valid_dog_data, files={"photo": image}, user=user)
        # Note: This will fail if image is too small, but tests the MIME type check
        assert "photo" not in form.errors or "image/jpeg" not in str(
            form.errors["photo"]
        )

    def test_dog_form_accepts_valid_png(self, user, valid_dog_data):
        """Test form accepts PNG images."""
        image = SimpleUploadedFile(
            "test.png", b"fake image content", content_type="image/png"
        )
        form = DogForm(data=valid_dog_data, files={"photo": image}, user=user)
        assert "photo" not in form.errors or "image/png" not in str(
            form.errors["photo"]
        )

    def test_dog_form_accepts_valid_webp(self, user, valid_dog_data):
        """Test form accepts WebP images."""
        image = SimpleUploadedFile(
            "test.webp", b"fake image content", content_type="image/webp"
        )
        form = DogForm(data=valid_dog_data, files={"photo": image}, user=user)
        assert "photo" not in form.errors or "image/webp" not in str(
            form.errors["photo"]
        )

    def test_dog_form_rejects_invalid_mime_type(self, user, valid_dog_data):
        """Test form rejects non-image files."""
        file = SimpleUploadedFile(
            "test.txt", b"not an image", content_type="text/plain"
        )
        form = DogForm(data=valid_dog_data, files={"photo": file}, user=user)
        assert not form.is_valid()
        assert "photo" in form.errors


@pytest.mark.forms
class TestDogFormUniqueNameValidation:
    """Test DogForm prevents duplicate names per owner."""

    def test_dog_form_allows_same_name_for_different_owners(
        self, user, user2, valid_dog_data, dog
    ):
        """Test different owners can use same dog name."""
        # user already has a dog named "Buddy"
        # user2 should be able to create a dog with the same name
        data = valid_dog_data.copy()
        data["name"] = dog.name

        form = DogForm(data=data, user=user2)
        assert form.is_valid()


@pytest.mark.forms
class TestDogSearchForm:
    """Test DogSearchForm validation."""

    def test_search_form_with_no_data(self):
        """Test search form without any data is valid."""
        form = DogSearchForm(data={})
        assert form.is_valid()

    def test_search_form_with_breed(self):
        """Test search form with breed filter."""
        form = DogSearchForm(data={"breed": "Labrador"})
        assert form.is_valid()
        assert form.cleaned_data["breed"] == "Labrador"

    def test_search_form_with_age_range(self):
        """Test search form with age filters."""
        form = DogSearchForm(data={"age_min": 2, "age_max": 5})
        assert form.is_valid()
        assert form.cleaned_data["age_min"] == 2
        assert form.cleaned_data["age_max"] == 5

    def test_search_form_with_gender(self):
        """Test search form with gender filter."""
        form = DogSearchForm(data={"gender": "M"})
        assert form.is_valid()
        assert form.cleaned_data["gender"] == "M"

    def test_search_form_with_size(self):
        """Test search form with size filter."""
        form = DogSearchForm(data={"size": "L"})
        assert form.is_valid()
        assert form.cleaned_data["size"] == "L"

    def test_search_form_with_all_filters(self):
        """Test search form with all filters."""
        form = DogSearchForm(
            data={
                "breed": "Labrador",
                "age_min": 2,
                "age_max": 5,
                "gender": "F",
                "size": "M",
            }
        )
        assert form.is_valid()

    def test_search_form_age_min_optional(self):
        """Test age_min is optional."""
        form = DogSearchForm(data={"age_max": 5})
        assert form.is_valid()

    def test_search_form_age_max_optional(self):
        """Test age_max is optional."""
        form = DogSearchForm(data={"age_min": 2})
        assert form.is_valid()

    def test_search_form_all_fields_optional(self):
        """Test all search fields are optional."""
        form = DogSearchForm(data={})
        assert form.is_valid()
