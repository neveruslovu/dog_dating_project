from .base import *  # noqa


# Production-specific overrides
DEBUG = False

# Security headers and cookie settings
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=True)
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)

# Optional: trusted origins for CSRF (comma-separated list in env)
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# CORS configuration for production
CORS_ALLOWED_ORIGINS = [
    "https://127.0.0.1:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://localhost:8000",
]
CORS_ALLOW_CREDENTIALS = True
