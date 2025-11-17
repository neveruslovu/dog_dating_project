from django.test import TestCase
from menu_app.models import Menu, MenuItem
from dogs.models import Dog, UserProfile
from django.contrib.auth.models import User


class DatabaseOperationsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "testuser", "test@example.com", "testpassword"
        )

    def tearDown(self):
        # Clean up in case of test failures
        try:
            User.objects.filter(username="testuser").delete()
        except:
            pass

    def test_create_operations(self):
        # Test creating objects
        menu = Menu.objects.create(
            name="test_menu", description="test menu description"
        )
        self.assertIsNotNone(menu.id)
        self.assertEqual(menu.name, "test_menu")

        menu_item = MenuItem.objects.create(
            menu=menu, title="test menu item", url="/test"
        )
        self.assertIsNotNone(menu_item.id)
        self.assertEqual(menu_item.title, "test menu item")

        dog = Dog.objects.create(
            owner=self.user,
            name="test_dog",
            breed="test_breed",
            age=1,
            gender="M",
            size="S",
            temperament="test_temperament",
            looking_for="playmate",
            description="test_description",
        )
        self.assertIsNotNone(dog.id)
        self.assertEqual(dog.name, "test_dog")

        user_profile = UserProfile.objects.create(user=self.user, bio="test bio")
        self.assertIsNotNone(user_profile.id)
        self.assertEqual(user_profile.bio, "test bio")

    def test_read_operations(self):
        # Create test objects
        menu = Menu.objects.create(
            name="test_menu", description="test menu description"
        )
        menu_item = MenuItem.objects.create(
            menu=menu, title="test menu item", url="/test"
        )
        dog = Dog.objects.create(
            owner=self.user,
            name="test_dog",
            breed="test_breed",
            age=1,
            gender="M",
            size="S",
            temperament="test_temperament",
            looking_for="playmate",
            description="test_description",
        )
        user_profile = UserProfile.objects.create(user=self.user, bio="test bio")

        # Test reading objects
        menus = Menu.objects.all()
        self.assertTrue(len(menus) > 0)
        self.assertIn(menu, menus)

        menu_items = MenuItem.objects.all()
        self.assertTrue(len(menu_items) > 0)
        self.assertIn(menu_item, menu_items)

        dogs = Dog.objects.all()
        self.assertTrue(len(dogs) > 0)
        self.assertIn(dog, dogs)

        user_profiles = UserProfile.objects.all()
        self.assertTrue(len(user_profiles) > 0)
        self.assertIn(user_profile, user_profiles)

    def test_update_operations(self):
        # Create test objects
        menu = Menu.objects.create(
            name="test_menu", description="test menu description"
        )
        dog = Dog.objects.create(
            owner=self.user,
            name="test_dog",
            breed="test_breed",
            age=1,
            gender="M",
            size="S",
            temperament="test_temperament",
            looking_for="playmate",
            description="test_description",
        )

        # Test updating objects
        menu.description = "updated description"
        menu.save()
        updated_menu = Menu.objects.get(id=menu.id)
        self.assertEqual(updated_menu.description, "updated description")

        dog.age = 2
        dog.save()
        updated_dog = Dog.objects.get(id=dog.id)
        self.assertEqual(updated_dog.age, 2)

    def test_delete_operations(self):
        # Create test objects
        menu = Menu.objects.create(
            name="test_menu", description="test menu description"
        )
        dog = Dog.objects.create(
            owner=self.user,
            name="test_dog",
            breed="test_breed",
            age=1,
            gender="M",
            size="S",
            temperament="test_temperament",
            looking_for="playmate",
            description="test_description",
        )
        user_profile = UserProfile.objects.create(user=self.user, bio="test bio")

        # Store IDs for later verification
        menu_id = menu.id
        dog_id = dog.id
        user_profile_id = user_profile.id
        user_id = self.user.id

        # Test deleting objects
        menu.delete()
        with self.assertRaises(Menu.DoesNotExist):
            Menu.objects.get(id=menu_id)

        dog.delete()
        with self.assertRaises(Dog.DoesNotExist):
            Dog.objects.get(id=dog_id)

        user_profile.delete()
        with self.assertRaises(UserProfile.DoesNotExist):
            UserProfile.objects.get(id=user_profile_id)
