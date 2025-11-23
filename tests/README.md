# DogDating Test Suite

## 📊 Test Suite Overview

This comprehensive test suite provides maximum code coverage for the DogDating Django application, following enterprise-level testing best practices and QA engineering standards.

## 🎯 Current Status

### ✅ Completed

- **Test Infrastructure**
  - ✅ Pytest configuration ([`pytest.ini`](../pytest.ini))
  - ✅ Coverage configuration ([`.coveragerc`](../.coveragerc))
  - ✅ Shared fixtures ([`conftest.py`](conftest.py))
  - ✅ Test data factories ([`factories.py`](factories.py))
  - ✅ CI/CD pipeline ([`.github/workflows/tests.yml`](../.github/workflows/tests.yml))

- **Documentation**
  - ✅ Comprehensive test plan ([`TEST_PLAN.md`](TEST_PLAN.md))
  - ✅ Testing guide ([`TESTING.md`](../TESTING.md))
  - ✅ Test dependencies ([`requirements-test.txt`](../requirements-test.txt))

- **Model Tests** (Example Implementation)
  - ✅ Dog model comprehensive tests ([`test_models/test_dog.py`](test_models/test_dog.py))
    - CRUD operations ✅
    - Field validations ✅
    - Unique constraints ✅
    - Relationships ✅
    - Custom properties ✅
    - Edge cases ✅
    - Querysets ✅

### 📝 Ready to Implement

The following test modules are ready to be implemented following the patterns established in `test_dog.py`:

#### Model Tests (`test_models/`)

- `test_user_profile.py` - UserProfile model tests
- `test_match.py` - Match model and status workflow tests
- `test_favorite.py` - Favorite model tests
- `test_message.py` - Message model tests
- `test_menu.py` - Menu and MenuItem tests

#### View Tests (`test_views/`)

- `test_auth_views.py` - Authentication (login, logout, register)
- `test_dog_views.py` - Dog CRUD operations
- `test_profile_views.py` - User profile management
- `test_match_views.py` - Match listing and management
- `test_favorite_views.py` - Favorites management

#### Form Tests (`test_forms/`)

- `test_dog_forms.py` - DogForm, DogSearchForm
- `test_auth_forms.py` - Registration, login forms
- `test_profile_forms.py` - Profile editing forms

#### Service Tests (`test_services/`)

- `test_dog_service.py` - Dog service layer
- `test_favorites_service.py` - Favorites service
- `test_match_service.py` - Match service

#### Permission Tests (`test_permissions/`)

- `test_dog_permissions.py` - Dog ownership checks
- `test_view_permissions.py` - @login_required enforcement

#### API Tests (`test_api/`)

- `test_ajax_endpoints.py` - AJAX endpoints (favorite toggle, etc.)

#### Integration Tests (`test_integration/`)

- `test_user_journey.py` - Complete user workflows
- `test_match_workflow.py` - Match creation and acceptance
- `test_search_workflow.py` - Search and filter flow

#### Error Tests (`test_errors/`)

- `test_error_handlers.py` - 404, 500 error handlers

---

## 🚀 Quick Start

### Installation

```bash
# Install test dependencies
pip install -r requirements-test.txt
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest tests/test_models/test_dog.py

# Run tests by marker
pytest -m models
pytest -m unit
pytest -m integration
```

### Expected Results

With the current infrastructure, you should see:

```bash
======================== test session starts =========================
plugins: django-4.5.2, cov-4.1.0, xdist-3.3.1
collected X items

tests/test_models/test_dog.py .......................... [100%]

==================== X passed in Y.YYs =====================
```

---

## 📚 Key Files

| File | Purpose |
|------|---------|
| [`TEST_PLAN.md`](TEST_PLAN.md) | Complete testing strategy and roadmap |
| [`TESTING.md`](../TESTING.md) | Developer testing guide |
| [`conftest.py`](conftest.py) | Pytest fixtures (users, dogs, clients, etc.) |
| [`factories.py`](factories.py) | Factory Boy data generators |
| [`test_models/test_dog.py`](test_models/test_dog.py) | Reference implementation |

---

## 🏗️ Test Structure

### Fixture Architecture

Reusable fixtures in `conftest.py`:

```python
# Users
user, user2, user3, staff_user, superuser, anonymous_user

# Clients  
client, authenticated_client, staff_client, admin_client

# Models
dog, dog2, other_dog, inactive_dog, multiple_dogs
user_profile, user2_profile
pending_match, accepted_match, declined_match
favorite, multiple_favorites
message, read_message
menu, menu_item, guest_menu

# Form data
valid_dog_data, valid_user_data, valid_login_data, valid_profile_data

# Factories
create_dog, create_match, create_favorite
```

### Factory Functions

Test data generators in `factories.py`:

```python
# Factories
UserFactory, StaffUserFactory, SuperUserFactory
UserProfileFactory
DogFactory, InactiveDogFactory, PuppyFactory, SeniorDogFactory
MatchFactory, PendingMatchFactory, AcceptedMatchFactory
FavoriteFactory, MessageFactory

# Utility functions
create_user_with_dogs(num_dogs=3)
create_match_scenario()
create_favorites_scenario(user, num_favorites=5)
create_complete_user()
create_pagination_dataset(total_items=50)
```

---

## 📝 Writing New Tests

### Template for Model Tests

```python
"""Tests for X Model."""

import pytest
from django.core.exceptions import ValidationError
from dogs.models import X


@pytest.mark.models
@pytest.mark.unit
class TestXModel:
    """Test X model basic operations."""
    
    def test_x_creation(self):
        """Test creating X with valid data."""
        # Arrange
        data = {...}
        
        # Act
        instance = X.objects.create(**data)
        
        # Assert
        assert instance.id is not None
    
    def test_x_str_representation(self):
        """Test __str__ method."""
        instance = X(...)
        assert str(instance) == "expected"
```

### Template for View Tests

```python
"""Tests for X Views."""

import pytest
from django.urls import reverse


@pytest.mark.views
@pytest.mark.integration
class TestXViews:
    """Test X view endpoints."""
    
    def test_x_view_authenticated(self, authenticated_client):
        """Test view requires authentication."""
        url = reverse('app:view_name')
        response = authenticated_client.get(url)
        assert response.status_code == 200
    
    def test_x_view_anonymous_redirects(self, client):
        """Test anonymous user is redirected."""
        url = reverse('app:view_name')
        response = client.get(url)
        assert response.status_code == 302
```

---

## 🎯 Coverage Targets

| Component | Target | Status |
|-----------|--------|--------|
| **Overall** | ≥ 85% | 🎯 To achieve |
| **Models** | ≥ 90% | 🎯 To achieve |
| **Views** | ≥ 80% | 🎯 To achieve |
| **Forms** | ≥ 90% | 🎯 To achieve |
| **Services** | ≥ 95% | 🎯 To achieve |

---

## 🔧 Testing Tools

### Installed Packages

- **pytest** - Test framework
- **pytest-django** - Django integration
- **pytest-cov** - Coverage reporting
- **pytest-xdist** - Parallel execution
- **factory-boy** - Test data factories
- **Faker** - Realistic fake data

### Available Markers

```python
@pytest.mark.unit          # Fast unit tests
@pytest.mark.integration   # Integration tests
@pytest.mark.slow          # Slow-running tests
@pytest.mark.models        # Model tests
@pytest.mark.views         # View tests
@pytest.mark.forms         # Form tests
@pytest.mark.services      # Service tests
@pytest.mark.permissions   # Permission tests
@pytest.mark.api           # API/AJAX tests
```

### Usage Examples

```bash
# Run only unit tests
pytest -m unit

# Run all except slow tests
pytest -m "not slow"

# Run models and services
pytest -m "models or services"

# Parallel execution
pytest -n auto

# HTML coverage report
pytest --cov --cov-report=html
```

---

## 📖 Documentation

- **[TEST_PLAN.md](TEST_PLAN.md)** - Comprehensive testing strategy document
- **[TESTING.md](../TESTING.md)** - Complete developer testing guide
- **[Django Testing Docs](https://docs.djangoproject.com/en/4.2/topics/testing/)**
- **[Pytest Documentation](https://docs.pytest.org/)**
- **[Factory Boy Docs](https://factoryboy.readthedocs.io/)**

---

## 🤝 Contributing Tests

### Guidelines

1. **Follow the Template** - Use existing tests as reference
2. **Use Fixtures** - Don't duplicate test setup
3. **Use Factories** - Generate test data efficiently
4. **Add Markers** - Categorize your tests
5. **Write Docstrings** - Document test purpose
6. **Test Edge Cases** - Don't just test happy paths
7. **Keep Tests Fast** - Mock external dependencies
8. **One Assert Per Test** - Focused, clear tests

### Before Submitting

```bash
# Run full test suite
pytest

# Check coverage
pytest --cov --cov-fail-under=80

# Run code quality checks
flake8 tests/
black tests/
isort tests/
```

---

## 🐛 Troubleshooting

### Common Issues

**Tests not discovered:**

```bash
# Check pytest.ini configuration
pytest --collect-only
```

**Import errors:**

```bash
# Ensure DJANGO_SETTINGS_MODULE is set
export DJANGO_SETTINGS_MODULE=project.settings.development
pytest
```

**Fixture errors:**

```bash
# List all available fixtures
pytest --fixtures
```

**Slow tests:**

```bash
# Find slowest tests
pytest --durations=10

# Run in parallel
pytest -n auto
```

For more troubleshooting, see [`TESTING.md`](../TESTING.md).

---

## 📊 CI/CD Integration

Tests run automatically via GitHub Actions on:

- Push to `main` or `develop`
- Pull requests

View workflow: [`.github/workflows/tests.yml`](../.github/workflows/tests.yml)

---

## 🎓 Learning Resources

- Start with [`test_models/test_dog.py`](test_models/test_dog.py) as reference
- Review fixtures in [`conftest.py`](conftest.py)
- Study factories in [`factories.py`](factories.py)
- Read [`TEST_PLAN.md`](TEST_PLAN.md) for strategy
- Follow [`TESTING.md`](../TESTING.md) for guide

---

**Next Steps:**

1. Install dependencies: `pip install -r requirements-test.txt`
2. Run existing tests: `pytest`
3. Implement additional test modules following established patterns
4. Achieve ≥85% overall coverage

**Questions?** See [`TESTING.md`](../TESTING.md) or review [`TEST_PLAN.md`](TEST_PLAN.md)

---

*Last Updated: 2025-11-22*
