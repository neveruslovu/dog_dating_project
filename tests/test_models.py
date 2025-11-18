import os
import sys
import django
from django.conf import settings

# Add parent directory to path if running standalone
if __name__ == "__main__" or not settings.configured:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

# Setup Django if not configured
if not settings.configured:
    django.setup()

from django.test import TestCase
from menu_app.models import Menu, MenuItem
from dogs.models import Dog
from django.contrib.auth.models import User


class MenuModelTest(TestCase):
    def test_menu_creation(self):
        menu = Menu.objects.create(name="Test Menu", description="Test Description")
        self.assertEqual(menu.name, "Test Menu")
        self.assertEqual(menu.description, "Test Description")
        self.assertIsNotNone(menu.id)

    def test_menu_str(self):
        menu = Menu.objects.create(name="Test Menu", description="Test Description")
        self.assertEqual(str(menu), "Test Menu")

    def test_menu_update(self):
        menu = Menu.objects.create(name="Test Menu", description="Test Description")
        menu.description = "Updated Description"
        menu.save()
        updated_menu = Menu.objects.get(id=menu.id)
        self.assertEqual(updated_menu.description, "Updated Description")

    def test_menu_deletion(self):
        menu = Menu.objects.create(name="Test Menu", description="Test Description")
        menu_id = menu.id
        menu.delete()
        with self.assertRaises(Menu.DoesNotExist):
            Menu.objects.get(id=menu_id)


class MenuItemModelTest(TestCase):
    def setUp(self):
        self.menu = Menu.objects.create(name="Parent Menu", description="Parent")

    def test_menuitem_creation(self):
        item = MenuItem.objects.create(title="Test Item", url="/test/", menu=self.menu)
        self.assertEqual(item.title, "Test Item")
        self.assertEqual(item.url, "/test/")
        self.assertEqual(item.menu, self.menu)

    def test_menuitem_str(self):
        item = MenuItem.objects.create(title="Test Item", url="/test/", menu=self.menu)
        self.assertEqual(str(item), "Test Item")

    def test_menuitem_update(self):
        item = MenuItem.objects.create(title="Test Item", url="/test/", menu=self.menu)
        item.title = "Updated Item"
        item.save()
        updated_item = MenuItem.objects.get(id=item.id)
        self.assertEqual(updated_item.title, "Updated Item")

    def test_menuitem_deletion(self):
        item = MenuItem.objects.create(title="Test Item", url="/test/", menu=self.menu)
        item_id = item.id
        item.delete()
        with self.assertRaises(MenuItem.DoesNotExist):
            MenuItem.objects.get(id=item_id)


class DogModelTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="dogowner", email="owner@example.com", password="test123"
        )

    def tearDown(self):
        self.owner.delete()

    def test_dog_creation(self):
        dog = Dog.objects.create(
            name="Test Dog",
            age=3,
            breed="Test Breed",
            description="Test Description",
            owner=self.owner,
            gender="M",
            size="M",
            temperament="friendly",
            looking_for="playmate",
        )
        self.assertEqual(dog.name, "Test Dog")
        self.assertEqual(dog.age, 3)
        self.assertEqual(dog.breed, "Test Breed")
        self.assertEqual(dog.owner, self.owner)

    def test_dog_str(self):
        dog = Dog.objects.create(
            name="Test Dog",
            age=3,
            breed="Test Breed",
            description="Test Description",
            owner=self.owner,
            gender="M",
            size="M",
            temperament="friendly",
            looking_for="playmate",
        )
        # Dog.__str__ now includes the owner username, per domain requirements
        self.assertEqual(str(dog), "Test Dog (dogowner)")

    def test_dog_update(self):
        dog = Dog.objects.create(
            name="Test Dog",
            age=3,
            breed="Test Breed",
            description="Test Description",
            owner=self.owner,
            gender="M",
            size="M",
            temperament="friendly",
            looking_for="playmate",
        )
        dog.age = 4
        dog.save()
        updated_dog = Dog.objects.get(id=dog.id)
        self.assertEqual(updated_dog.age, 4)

    def test_dog_deletion(self):
        dog = Dog.objects.create(
            name="Test Dog",
            age=3,
            breed="Test Breed",
            description="Test Description",
            owner=self.owner,
            gender="M",
            size="M",
            temperament="friendly",
            looking_for="playmate",
        )
        dog_id = dog.id
        dog.delete()
        with self.assertRaises(Dog.DoesNotExist):
            Dog.objects.get(id=dog_id)


class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))

    def test_user_str(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.assertEqual(str(user), "testuser")

    def test_user_update(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        user.email = "updated@example.com"
        user.save()
        updated_user = User.objects.get(id=user.id)
        self.assertEqual(updated_user.email, "updated@example.com")

    def test_user_deletion(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        user_id = user.id
        user.delete()
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=user_id)
