from .base import *  # noqa


# Development-specific overrides
DEBUG = env.bool("DEBUG", default=True)
