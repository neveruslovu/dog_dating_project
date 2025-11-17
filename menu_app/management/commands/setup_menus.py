# menu_app/management/commands/setup_menus.py
from django.core.management.base import BaseCommand
from menu_app.models import Menu, MenuItem


class Command(BaseCommand):
    help = "Создает начальную структуру меню"

    def handle(self, *args, **options):
        # Главное меню
        main_menu, _ = Menu.objects.get_or_create(
            name="main_menu", defaults={"description": "Главное меню сайта"}
        )

        # Создаем пункты главного меню
        home = MenuItem.objects.create(
            menu=main_menu, title="Главная", named_url="dogs:home", order=1
        )

        dogs = MenuItem.objects.create(
            menu=main_menu, title="Собаки", named_url="dogs:dog_list", order=2
        )

        MenuItem.objects.create(
            menu=main_menu,
            parent=dogs,
            title="Регистрация собаки",
            named_url="dogs:register",
            order=1,
        )

        MenuItem.objects.create(
            menu=main_menu,
            parent=dogs,
            title="Найти пару",
            named_url="dogs:dog_list",
            order=2,
        )

        MenuItem.objects.create(
            menu=main_menu,
            parent=dogs,
            title="Все породы",
            named_url="dogs:breeds",
            order=3,
        )

        info = MenuItem.objects.create(
            menu=main_menu, title="Информация", named_url="dogs:about", order=3
        )

        MenuItem.objects.create(
            menu=main_menu,
            parent=info,
            title="О сервисе",
            named_url="dogs:about",
            order=1,
        )

        MenuItem.objects.create(
            menu=main_menu,
            parent=info,
            title="Мероприятия",
            named_url="dogs:events",
            order=2,
        )

        MenuItem.objects.create(
            menu=main_menu, parent=info, title="Советы", named_url="dogs:tips", order=3
        )

        # Футер меню - ИСПРАВЛЯЕМ URL НА NAMED_URL
        footer_menu, _ = Menu.objects.get_or_create(
            name="footer_menu", defaults={"description": "Меню в футере"}
        )

        MenuItem.objects.create(
            menu=footer_menu, title="Контакты", named_url="dogs:contacts", order=1
        )

        MenuItem.objects.create(
            menu=footer_menu,
            title="Политика конфиденциальности",
            named_url="dogs:privacy",
            order=2,
        )

        self.stdout.write(self.style.SUCCESS("Меню успешно созданы!"))
