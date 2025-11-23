#!/usr/bin/env python
"""
Verification script for static files configuration.
Run this script to verify that static files are properly configured for production.
"""
import os
import sys
from pathlib import Path

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.production")

# Setup Django
import django

django.setup()

from django.conf import settings
from django.core.management import call_command


def check_paths():
    """Verify that paths are correctly configured."""
    print("=" * 60)
    print("CHECKING PATHS")
    print("=" * 60)

    checks = []

    # Check BASE_DIR
    expected_base = Path(__file__).resolve().parent
    actual_base = Path(settings.BASE_DIR)
    base_ok = expected_base == actual_base
    checks.append(base_ok)
    print(
        f"✓ BASE_DIR correct: {actual_base}"
        if base_ok
        else f"✗ BASE_DIR incorrect: {actual_base}"
    )

    # Check STATIC_ROOT
    static_root = Path(settings.STATIC_ROOT)
    static_ok = static_root == expected_base / "staticfiles"
    checks.append(static_ok)
    print(
        f"✓ STATIC_ROOT correct: {static_root}"
        if static_ok
        else f"✗ STATIC_ROOT incorrect: {static_root}"
    )

    # Check STATIC_URL
    static_url_ok = (
        settings.STATIC_URL == "/static/" or settings.STATIC_URL == "static/"
    )
    checks.append(static_url_ok)
    print(
        f"✓ STATIC_URL: {settings.STATIC_URL}"
        if static_url_ok
        else f"✗ STATIC_URL incorrect: {settings.STATIC_URL}"
    )

    return all(checks)


def check_middleware():
    """Verify WhiteNoise middleware is installed."""
    print("\n" + "=" * 60)
    print("CHECKING MIDDLEWARE")
    print("=" * 60)

    middleware_list = settings.MIDDLEWARE
    has_whitenoise = any("whitenoise" in m.lower() for m in middleware_list)

    if has_whitenoise:
        whitenoise_index = next(
            i for i, m in enumerate(middleware_list) if "whitenoise" in m.lower()
        )
        security_index = next(
            (i for i, m in enumerate(middleware_list) if "SecurityMiddleware" in m), -1
        )

        if security_index >= 0 and whitenoise_index == security_index + 1:
            print(
                "✓ WhiteNoise middleware correctly positioned after SecurityMiddleware"
            )
            return True
        else:
            print("⚠ WhiteNoise middleware found but not in optimal position")
            return True
    else:
        print("✗ WhiteNoise middleware not found")
        return False


def check_storage():
    """Verify STORAGES configuration."""
    print("\n" + "=" * 60)
    print("CHECKING STORAGE BACKENDS")
    print("=" * 60)

    storages = getattr(settings, "STORAGES", {})
    staticfiles_backend = storages.get("staticfiles", {}).get("BACKEND", "")

    if "whitenoise" in staticfiles_backend.lower():
        print(f"✓ WhiteNoise storage backend configured: {staticfiles_backend}")
        return True
    else:
        print(
            f"⚠ WhiteNoise storage backend not configured. Using: {staticfiles_backend or 'default'}"
        )
        return False


def check_static_files():
    """Verify that static files have been collected."""
    print("\n" + "=" * 60)
    print("CHECKING COLLECTED STATIC FILES")
    print("=" * 60)

    static_root = Path(settings.STATIC_ROOT)

    if not static_root.exists():
        print(f"⚠ Static files directory does not exist: {static_root}")
        print("  Run: python manage.py collectstatic")
        return False

    # Check for admin static files
    admin_css = static_root / "admin" / "css"
    if not admin_css.exists():
        print(f"✗ Admin CSS directory not found: {admin_css}")
        return False

    css_files = list(admin_css.glob("*.css")) + list(admin_css.glob("*.css.gz"))
    print(f"✓ Found {len(css_files)} admin CSS files in {admin_css}")

    # Check for manifest file (created by WhiteNoise)
    manifest = static_root / "staticfiles.json"
    if manifest.exists():
        print(f"✓ WhiteNoise manifest found: {manifest}")
    else:
        print(
            f"⚠ WhiteNoise manifest not found (will be created on next collectstatic)"
        )

    return True


def main():
    """Run all verification checks."""
    print("Django Static Files Verification Script")
    print("Settings:", os.environ.get("DJANGO_SETTINGS_MODULE"))
    print()

    results = []

    # Run checks
    results.append(("Paths", check_paths()))
    results.append(("Middleware", check_middleware()))
    results.append(("Storage", check_storage()))
    results.append(("Static Files", check_static_files()))

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    all_passed = all(result for _, result in results)

    if all_passed:
        print("\n✅ All checks passed! Static files are properly configured.")
        return 0
    else:
        print("\n⚠ Some checks failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
