"""
Menu and MenuItem Model Tests

Tests for the menu_app models.
"""

import pytest
from django.test import TestCase
from menu_app.models import Menu, MenuItem


@pytest.mark.models
@pytest.mark.unit
class TestMenuModel:
    """Test suite for Menu model."""

    def test_menu_creation(self, db):
        """Test creating a menu."""
        menu = Menu.objects.create(name="Test Menu", description="Test Description")
        assert menu.name == "Test Menu"
        assert menu.description == "Test Description"
        assert menu.id is not None

    def test_menu_str(self, db):
        """Test menu string representation."""
        menu = Menu.objects.create(name="Test Menu", description="Test Description")
        assert str(menu) == "Test Menu"

    def test_menu_update(self, db):
        """Test updating menu."""
        menu = Menu.objects.create(name="Test Menu", description="Test Description")
        menu.description = "Updated Description"
        menu.save()
        updated_menu = Menu.objects.get(id=menu.id)
        assert updated_menu.description == "Updated Description"

    def test_menu_deletion(self, db):
        """Test deleting menu."""
        menu = Menu.objects.create(name="Test Menu", description="Test Description")
        menu_id = menu.id
        menu.delete()
        with pytest.raises(Menu.DoesNotExist):
            Menu.objects.get(id=menu_id)


@pytest.mark.models
@pytest.mark.unit
class TestMenuItemModel:
    """Test suite for MenuItem model."""

    @pytest.fixture
    def menu(self, db):
        """Create a parent menu for tests."""
        return Menu.objects.create(name="Parent Menu", description="Parent")

    def test_menuitem_creation(self, menu):
        """Test creating a menu item."""
        item = MenuItem.objects.create(title="Test Item", url="/test/", menu=menu)
        assert item.title == "Test Item"
        assert item.url == "/test/"
        assert item.menu == menu

    def test_menuitem_str(self, menu):
        """Test menu item string representation."""
        item = MenuItem.objects.create(title="Test Item", url="/test/", menu=menu)
        assert str(item) == "Test Item"

    def test_menuitem_update(self, menu):
        """Test updating menu item."""
        item = MenuItem.objects.create(title="Test Item", url="/test/", menu=menu)
        item.title = "Updated Item"
        item.save()
        updated_item = MenuItem.objects.get(id=item.id)
        assert updated_item.title == "Updated Item"

    def test_menuitem_deletion(self, menu):
        """Test deleting menu item."""
        item = MenuItem.objects.create(title="Test Item", url="/test/", menu=menu)
        item_id = item.id
        item.delete()
        with pytest.raises(MenuItem.DoesNotExist):
            MenuItem.objects.get(id=item_id)

    def test_menuitem_relationship(self, menu):
        """Test menu item relationship with menu."""
        item = MenuItem.objects.create(title="Test Item", url="/test/", menu=menu)
        assert item in menu.items.all()
