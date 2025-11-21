from .base import *  # noqa


# Development-specific overrides
DEBUG = env.bool("DEBUG", default=True)

# CORS configuration for development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
