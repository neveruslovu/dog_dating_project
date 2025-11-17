#!/usr/bin/env python
"""
Guest Menu Implementation - Step-by-Step Integration Test Script
This script validates that the guest menu implementation is correctly integrated.
Run this to ensure all components are in place and working.
"""

import os
import re
from pathlib import Path


def check_file_exists(filepath, description=""):
    """Check if a file exists."""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"✅ {description}: {filepath} ({size} bytes)")
        return True
    else:
        print(f"❌ {description}: {filepath} NOT FOUND")
        return False


def check_content_in_file(filepath, pattern, description="", is_regex=False):
    """Check if content exists in a file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if is_regex:
            if re.search(pattern, content):
                print(f"  ✅ {description}")
                return True
            else:
                print(f"  ❌ {description}")
                return False
        else:
            if pattern in content:
                print(f"  ✅ {description}")
                return True
            else:
                print(f"  ❌ {description}")
                return False
    except Exception as e:
        print(f"  ❌ Error checking {filepath}: {e}")
        return False


def main():
    print("=" * 70)
    print("GUEST MENU IMPLEMENTATION VALIDATION")
    print("=" * 70)
    print()

    base_path = Path(__file__).parent

    # Step 1: Check files exist
    print("STEP 1: Checking Files...")
    print("-" * 70)

    files_ok = all(
        [
            check_file_exists(
                base_path
                / "dogs"
                / "templates"
                / "dogs"
                / "components"
                / "guest_menu.html",
                "Guest menu component",
            ),
            check_file_exists(
                base_path / "dogs" / "templates" / "dogs" / "base.html", "Base template"
            ),
        ]
    )
    print()

    # Step 2: Check base.html modifications
    print("STEP 2: Checking base.html Modifications...")
    print("-" * 70)

    base_html_path = base_path / "dogs" / "templates" / "dogs" / "base.html"
    base_ok = all(
        [
            check_content_in_file(
                base_html_path,
                "guest-menu-container",
                "Guest menu CSS container class present",
            ),
            check_content_in_file(
                base_html_path,
                "{% include 'dogs/components/guest_menu.html' %}",
                "Guest menu component included in header",
            ),
            check_content_in_file(
                base_html_path,
                "GUEST_MENU_ENABLED",
                "Feature flag present in JavaScript",
            ),
            check_content_in_file(
                base_html_path,
                "initGuestMenu",
                "Guest menu initialization function present",
            ),
            check_content_in_file(
                base_html_path,
                "guest-menu-toggle",
                "Guest menu toggle CSS class defined",
            ),
        ]
    )
    print()

    # Step 3: Check guest_menu.html content
    print("STEP 3: Checking guest_menu.html Content...")
    print("-" * 70)

    guest_menu_path = (
        base_path / "dogs" / "templates" / "dogs" / "components" / "guest_menu.html"
    )
    guest_ok = all(
        [
            check_content_in_file(
                guest_menu_path, "guest-menu-dropdown", "Dropdown container present"
            ),
            check_content_in_file(
                guest_menu_path,
                'role="navigation"',
                "Navigation role present (accessibility)",
            ),
            check_content_in_file(
                guest_menu_path, "{% url 'dogs:about' %}", "About link present"
            ),
            check_content_in_file(
                guest_menu_path, "{% url 'dogs:login' %}", "Login link present"
            ),
            check_content_in_file(
                guest_menu_path, "{% url 'dogs:register' %}", "Register link present"
            ),
        ]
    )
    print()

    # Step 4: Check for conflicts
    print("STEP 4: Checking for Potential Conflicts...")
    print("-" * 70)

    conflicts_ok = True

    # Check authenticated menu is still present
    if check_content_in_file(
        base_html_path,
        "user.is_authenticated",
        "Authenticated user check still present",
    ):
        pass
    else:
        conflicts_ok = False

    # Check sidebar is still present
    if check_content_in_file(
        base_html_path,
        'class="sidebar"',
        "Sidebar for authenticated users still present",
    ):
        pass
    else:
        conflicts_ok = False

    # Check menu-link class (authenticated menu) is unchanged
    if check_content_in_file(
        base_html_path, 'class="menu-link"', "Authenticated menu links still present"
    ):
        pass
    else:
        conflicts_ok = False

    print()

    # Step 5: Check accessibility
    print("STEP 5: Checking Accessibility Features...")
    print("-" * 70)

    accessibility_ok = all(
        [
            check_content_in_file(
                guest_menu_path, "aria-expanded", "ARIA expanded attribute present"
            ),
            check_content_in_file(
                guest_menu_path, "aria-hidden", "ARIA hidden attribute present"
            ),
            check_content_in_file(guest_menu_path, 'role="menu"', "Menu role present"),
            check_content_in_file(
                guest_menu_path, 'role="menuitem"', "Menu item role present"
            ),
        ]
    )
    print()

    # Step 6: Check responsive design
    print("STEP 6: Checking Responsive Design...")
    print("-" * 70)

    responsive_ok = all(
        [
            check_content_in_file(
                base_html_path,
                "@media (max-width: 768px)",
                "Tablet breakpoint styles present",
                is_regex=True,
            ),
            check_content_in_file(
                base_html_path,
                "@media (max-width: 480px)",
                "Mobile breakpoint styles present",
                is_regex=True,
            ),
        ]
    )
    print()

    # Final summary
    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)

    all_checks = {
        "Files Present": files_ok,
        "base.html Modifications": base_ok,
        "guest_menu.html Content": guest_ok,
        "No Conflicts": conflicts_ok,
        "Accessibility": accessibility_ok,
        "Responsive Design": responsive_ok,
    }

    for check_name, result in all_checks.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name}: {status}")

    print()

    if all(all_checks.values()):
        print("🎉 ALL CHECKS PASSED! Guest menu is correctly integrated.")
        return 0
    else:
        print("⚠️  SOME CHECKS FAILED. Please review the implementation.")
        return 1


if __name__ == "__main__":
    exit(main())
