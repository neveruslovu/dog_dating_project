from django.test import TestCase
from django.db import models
import os
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from menu_app.models import Menu, MenuItem
from dogs.models import Dog
from django.contrib.auth.models import User


def test_menu_models():
    print("Testing Menu model...")
    try:
        # Create
        menu = Menu.objects.create(name="Test Menu", description="Test Description")
        print(f"✓ Created Menu: {menu}")

        # Read
        menus = Menu.objects.all()
        print(f"✓ All menus: {len(menus)}")

        # Update
        menu.description = "Updated Description"
        menu.save()
        print(f"✓ Updated Menu: {menu}")

        # Delete
        menu_id = menu.id
        menu.delete()
        print(f"✓ Deleted Menu with id: {menu_id}")

    except Exception as e:
        print(f"✗ Menu model error: {e}")


def test_menuitem_models():
    print("Testing MenuItem model...")

    # First create a menu
    menu = Menu.objects.create(name="Parent Menu", description="Parent")

    try:
        # Create standalone menu item
        item = MenuItem.objects.create(title="Test Item", url="/test/", menu=menu)
        print(f"✓ Created MenuItem: {item}")

        # Update
        item.title = "Updated Item"
        item.save()
        print(f"✓ Updated MenuItem: {item}")

        # Delete
        item_id = item.id
        item.delete()
        print(f"✓ Deleted MenuItem with id: {item_id}")

        menu.delete()  # Clean up

    except Exception as e:
        print(f"✗ MenuItem model error: {e}")
        menu.delete()


def test_dog_models():
    print("Testing Dog model...")
    # Create a user first for owner
    owner = User.objects.create_user(
        username="dogowner", email="owner@example.com", password="test123"
    )
    try:
        # Dog model requires additional fields: gender, size, temperament, looking_for
        dog = Dog.objects.create(
            name="Test Dog",
            age=3,
            breed="Test Breed",
            description="Test Description",
            owner=owner,
            gender="M",
            size="M",
            temperament="friendly",
            looking_for="playmate",
        )
        print(f"✓ Created Dog: {dog}")

        dogs = Dog.objects.all()
        print(f"✓ All dogs: {len(dogs)}")

        dog.age = 4
        dog.save()
        print(f"✓ Updated Dog: {dog}")

        dog_id = dog.id
        dog.delete()
        print(f"✓ Deleted Dog with id: {dog_id}")
        owner.delete()  # Clean up owner

    except Exception as e:
        print(f"✗ Dog model error: {e}")
        owner.delete()


def test_user_models():
    print("Testing User model...")
    try:
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        print(f"✓ Created User: {user}")

        users = User.objects.all()
        print(f"✓ All users: {len(users)}")

        user.email = "updated@example.com"
        user.save()
        print(f"✓ Updated User: {user}")

        user_id = user.id
        user.delete()
        print(f"✓ Deleted User with id: {user_id}")

    except Exception as e:
        print(f"✗ User model error: {e}")


if __name__ == "__main__":
    print("=== Testing Models ===")
    test_menu_models()
    print()
    test_menuitem_models()
    print()
    test_dog_models()
    print()
    test_user_models()
    print("=== Done ===")
