"""
Test-specific Django settings that override base settings for pytest.

This configuration ensures tests run with an in-memory SQLite database
regardless of the DATABASE_URL environment variable, making tests:
- Fast (in-memory database)
- Isolated (no Docker required)
- Portable (works on any machine)
"""

from .base import *  # noqa

# Force SQLite in-memory database for tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Disable debug mode in tests for performance
DEBUG = False

# Simplify password hashing for faster tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]


# Disable migrations for faster test database creation
# (Only use if you don't need migration-specific tests)
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


# Uncomment to disable migrations (faster but less thorough)
# MIGRATION_MODULES = DisableMigrations()

# Email backend for tests
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Media files for tests
MEDIA_ROOT = BASE_DIR / "test_media"

# Disable whitenoise for tests (faster)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
