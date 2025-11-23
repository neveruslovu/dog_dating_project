#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Setup Verification Script

Verifies that the test infrastructure is correctly configured and ready to use.
Run this before executing actual tests to catch configuration issues early.
"""

import os
import sys
from pathlib import Path

# Set UTF-8 encoding for Windows
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_check(status, message):
    """Print a check result."""
    icon = "[OK]" if status else "[FAIL]"
    print(f"{icon} {message}")
    return status


def check_file_exists(filepath, description):
    """Check if a file exists."""
    exists = Path(filepath).exists()
    return print_check(exists, f"{description}: {filepath}")


def check_directory_exists(dirpath, description):
    """Check if a directory exists."""
    exists = Path(dirpath).is_dir()
    return print_check(exists, f"{description}: {dirpath}")


def check_python_import(module_name):
    """Check if a Python module can be imported."""
    try:
        __import__(module_name)
        return print_check(True, f"Module '{module_name}' can be imported")
    except ImportError as e:
        print_check(False, f"Module '{module_name}' import failed: {e}")
        return False


def main():
    """Run all verification checks."""
    print_header("Test Infrastructure Verification")

    all_checks = []

    # Check configuration files
    print("\n📋 Configuration Files:")
    all_checks.append(check_file_exists("pytest.ini", "Pytest configuration"))
    all_checks.append(check_file_exists(".coveragerc", "Coverage configuration"))
    all_checks.append(check_file_exists("requirements-test.txt", "Test dependencies"))
    all_checks.append(
        check_file_exists(".github/workflows/tests.yml", "CI/CD workflow")
    )

    # Check test directories
    print("\n📁 Test Directories:")
    all_checks.append(check_directory_exists("tests", "Tests directory"))
    all_checks.append(check_directory_exists("tests/test_models", "Model tests"))
    all_checks.append(check_directory_exists("tests/test_views", "View tests"))
    all_checks.append(check_directory_exists("tests/test_forms", "Form tests"))
    all_checks.append(check_directory_exists("tests/test_api", "API tests"))
    all_checks.append(
        check_directory_exists("tests/test_integration", "Integration tests")
    )
    all_checks.append(
        check_directory_exists("tests/test_permissions", "Permission tests")
    )
    all_checks.append(check_directory_exists("tests/test_errors", "Error tests"))

    # Check test files
    print("\n[Test Files]")
    all_checks.append(check_file_exists("tests/conftest.py", "Pytest fixtures"))
    all_checks.append(check_file_exists("tests/factories.py", "Factory definitions"))
    all_checks.append(check_file_exists("tests/utils.py", "Test utilities"))
    all_checks.append(
        check_file_exists("tests/test_models/test_dog.py", "Dog model tests")
    )
    all_checks.append(
        check_file_exists("tests/test_views/test_auth_views.py", "Auth view tests")
    )
    all_checks.append(
        check_file_exists("tests/test_views/test_dog_views.py", "Dog view tests")
    )
    all_checks.append(
        check_file_exists("tests/test_forms/test_dog_forms.py", "Dog form tests")
    )
    all_checks.append(
        check_file_exists("tests/test_api/test_ajax_endpoints.py", "AJAX tests")
    )
    all_checks.append(
        check_file_exists(
            "tests/test_integration/test_user_journey.py", "Integration tests"
        )
    )
    all_checks.append(
        check_file_exists(
            "tests/test_permissions/test_dog_permissions.py", "Permission tests"
        )
    )

    # Check documentation
    print("\n[Documentation]")
    all_checks.append(check_file_exists("tests/TEST_PLAN.md", "Test plan"))
    all_checks.append(check_file_exists("TESTING.md", "Testing guide"))
    all_checks.append(check_file_exists("tests/README.md", "Test suite README"))

    # Check Django setup
    print("\n[Django Configuration]")
    try:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.development")
        import django

        django.setup()
        print_check(True, "Django setup successful")
        all_checks.append(True)
    except Exception as e:
        print_check(False, f"Django setup failed: {e}")
        all_checks.append(False)

    # Check imports
    print("\n[Django Apps]")
    all_checks.append(check_python_import("dogs"))
    all_checks.append(check_python_import("menu_app"))
    all_checks.append(check_python_import("services.dog_service"))

    # Summary
    print_header("Verification Summary")
    passed = sum(all_checks)
    total = len(all_checks)
    percentage = (passed / total * 100) if total > 0 else 0

    print(f"\n[PASSED] {passed}/{total} ({percentage:.1f}%)")

    if passed == total:
        print("\n[SUCCESS] All checks passed! Test infrastructure is ready.")
        print("\n[Next steps]")
        print("   1. Install test dependencies: pip install -r requirements-test.txt")
        print("   2. Run tests: pytest")
        print("   3. Check coverage: pytest --cov")
        return 0
    else:
        failed = total - passed
        print(f"\n[WARNING] {failed} check(s) failed. Please review the errors above.")
        print("\n[Common fixes]")
        print("   - Ensure you're in the project root directory")
        print("   - Check that all files were created correctly")
        print("   - Verify Django is properly configured")
        return 1


if __name__ == "__main__":
    sys.exit(main())
