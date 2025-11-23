from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from . import views_new

app_name = "dogs"

urlpatterns = [
    # Главные страницы
    path("", views.landing_page, name="landing_page"),
    path("home/", views.home, name="home"),
    # Аутентификация
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    # Личный кабинет
    path("dashboard/", views.dashboard, name="dashboard"),
    # Профиль пользователя
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("change-password/", views.change_password, name="change_password"),
    path("delete-account/", views.delete_account, name="delete_account"),
    # CRUD операции с собаками
    path("dogs/", views.dog_list, name="dog_list"),
    path("dogs/create/", views.dog_create, name="dog_create"),
    path("dogs/<int:pk>/", views.dog_detail, name="dog_detail"),
    path("dogs/<int:pk>/edit/", views.dog_update, name="dog_update"),
    path("dogs/<int:pk>/delete/", views.dog_delete, name="dog_delete"),
    # Взаимодействия с собаками
    path("dogs/<int:pk>/favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("matches/", views.matches_list, name="matches_list"),
    path("favorites/", views.favorites_list, name="favorites_list"),
    # Старые URL (для совместимости - удалить после тестирования)
    # path("register/", views.register_dog, name="register_old"),
    # path("profile/<int:dog_id>/", views.dog_profile, name="profile_old"),
    # Информационные страницы
    path("about/", views.about, name="about"),
    path("breeds/", views.breeds, name="breeds"),
    path("events/", views.events, name="events"),
    path("tips/", views.tips, name="tips"),
    # Дополнительные страницы для меню - FIX 404 ERRORS
    path("contacts/", views_new.contacts, name="contacts"),
    path("privacy/", views_new.privacy, name="privacy"),
]
