from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from services.favorites_service import toggle_favorite_for_user
from .models import Dog, UserProfile, Match, Favorite
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    DogForm,
    UserProfileForm,
    PasswordChangeForm,
    AccountDeletionForm,
    DogSearchForm,
)


def landing_page(request):
    """Главная страница для неавторизованных пользователей"""
    # Fix admin authentication separation: logout staff users (admin panel users)
    # to prevent admin auto-login on frontend
    if request.user.is_authenticated and request.user.is_staff:
        from django.contrib.auth import logout

        logout(request)
        return redirect("dogs:landing_page")

    if request.user.is_authenticated:
        return redirect("dogs:dashboard")

    # Получаем несколько случайных собак для демонстрации
    featured_dogs = Dog.objects.filter(is_active=True).order_by("?")[:6]

    return render(request, "dogs/landing.html", {"featured_dogs": featured_dogs})


def register(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect("dogs:dashboard")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f"Добро пожаловать, {user.username}! Создайте профиль своей собаки.",
            )
            return redirect("dogs:dashboard")
    else:
        form = UserRegistrationForm()

    return render(request, "dogs/register.html", {"form": form, "title": "Регистрация"})


def user_login(request):
    """Вход пользователя в систему"""
    if request.user.is_authenticated:
        return redirect("dogs:dashboard")

    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # Настраиваем срок действия сессии
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 недели
                else:
                    request.session.set_expiry(0)  # До закрытия браузера

                messages.success(request, f"Добро пожаловать, {user.username}!")
                return redirect("dogs:dashboard")
            else:
                messages.error(request, "Неверное имя пользователя или пароль.")

    else:
        form = UserLoginForm()

    return render(request, "dogs/login.html", {"form": form, "title": "Вход"})


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    messages.info(request, "Вы успешно вышли из системы.")
    return redirect("dogs:landing_page")


@login_required
def dashboard(request):
    """Личный кабинет пользователя"""
    user_dogs = Dog.objects.filter(owner=request.user)
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]

    # Статистика
    total_matches = Match.objects.filter(
        Q(dog_from__owner=request.user) | Q(dog_to__owner=request.user)
    ).count()

    total_favorites = Favorite.objects.filter(user=request.user).count()

    # Недавние активности
    recent_matches = Match.objects.filter(
        Q(dog_from__owner=request.user) | Q(dog_to__owner=request.user)
    ).order_by("-created_at")[:5]

    context = {
        "user_dogs": user_dogs,
        "user_profile": user_profile,
        "total_matches": total_matches,
        "total_favorites": total_favorites,
        "recent_matches": recent_matches,
        "page_title": "Личный кабинет",
    }

    return render(request, "dogs/dashboard.html", context)


def home(request):
    """Главная страница"""
    if not request.user.is_authenticated:
        return redirect("dogs:landing_page")

    return render(request, "dogs/home.html")


def dog_list(request):
    """Список всех собак с фильтрами"""
    dogs = Dog.objects.filter(is_active=True).select_related("owner")
    search_form = DogSearchForm(request.GET)

    if search_form.is_valid():
        # Применяем фильтры
        breed = search_form.cleaned_data.get("breed")
        age_min = search_form.cleaned_data.get("age_min")
        age_max = search_form.cleaned_data.get("age_max")
        gender = search_form.cleaned_data.get("gender")
        size = search_form.cleaned_data.get("size")

        if breed:
            dogs = dogs.filter(breed__icontains=breed)

        if age_min is not None:
            dogs = dogs.filter(age__gte=age_min)

        if age_max is not None:
            dogs = dogs.filter(age__lte=age_max)

        if gender:
            dogs = dogs.filter(gender=gender)

        if size:
            dogs = dogs.filter(size=size)

    # Пагинация
    paginator = Paginator(dogs, 12)  # 12 собак на страницу
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "dogs/dog_list.html",
        {
            "page_obj": page_obj,
            "search_form": search_form,
            "total_results": dogs.count(),
        },
    )


def dog_detail(request, pk):
    """Подробная информация о собаке"""
    dog = get_object_or_404(Dog.objects.select_related("owner"), pk=pk, is_active=True)

    # Проверяем, добавлена ли собака в избранное
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, dog=dog).exists()

    return render(
        request,
        "dogs/dog_detail.html",
        {
            "dog": dog,
            "is_favorite": is_favorite,
            "can_edit": dog.owner == request.user,
        },
    )


@login_required
def dog_create(request):
    """Создание нового профиля собаки"""
    if request.method == "POST":
        form = DogForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            dog = form.save()
            messages.success(request, f'Профиль собаки "{dog.name}" успешно создан!')
            return redirect("dogs:dog_detail", pk=dog.pk)
    else:
        form = DogForm(user=request.user)

    return render(
        request,
        "dogs/dog_form.html",
        {"form": form, "title": "Добавить собаку", "submit_button": "Создать профиль"},
    )


@login_required
def dog_update(request, pk):
    """Редактирование профиля собаки"""
    dog = get_object_or_404(Dog, pk=pk, owner=request.user)

    if request.method == "POST":
        form = DogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            form.save()
            messages.success(request, f'Профиль собаки "{dog.name}" успешно обновлен!')
            return redirect("dogs:dog_detail", pk=dog.pk)
    else:
        form = DogForm(instance=dog)

    return render(
        request,
        "dogs/dog_form.html",
        {
            "form": form,
            "dog": dog,
            "title": "Редактировать профиль",
            "submit_button": "Сохранить изменения",
        },
    )


@login_required
def dog_delete(request, pk):
    """Удаление профиля собаки"""
    dog = get_object_or_404(Dog, pk=pk, owner=request.user)

    if request.method == "POST":
        dog_name = dog.name
        dog.delete()
        messages.success(request, f'Профиль собаки "{dog_name}" успешно удален.')
        return redirect("dogs:dashboard")

    return render(request, "dogs/dog_confirm_delete.html", {"dog": dog})


@login_required
def profile_view(request):
    """Просмотр профиля пользователя"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    return render(
        request,
        "dogs/profile.html",
        {"user_profile": user_profile, "page_title": "Мой профиль"},
    )


@login_required
def profile_edit(request):
    """Редактирование профиля пользователя"""
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен!")
            return redirect("dogs:profile")
    else:
        form = UserProfileForm(instance=user_profile)

    return render(
        request,
        "dogs/profile_edit.html",
        {"form": form, "user_profile": user_profile, "title": "Редактировать профиль"},
    )


@login_required
def change_password(request):
    """Изменение пароля"""
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data["old_password"]
            new_password = form.cleaned_data["new_password1"]

            # Проверяем текущий пароль
            if not request.user.check_password(old_password):
                messages.error(request, "Текущий пароль неверный.")
                return redirect("dogs:change_password")

            # Устанавливаем новый пароль
            request.user.set_password(new_password)
            request.user.save()

            # Обновляем сессию
            update_session_auth_hash(request, request.user)

            messages.success(request, "Пароль успешно изменен!")
            return redirect("dogs:profile")
    else:
        form = PasswordChangeForm()

    return render(
        request, "dogs/change_password.html", {"form": form, "title": "Изменить пароль"}
    )


@login_required
def delete_account(request):
    """Удаление аккаунта пользователя"""
    if request.method == "POST":
        form = AccountDeletionForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]

            # Проверяем пароль
            if not request.user.check_password(password):
                messages.error(request, "Неверный пароль.")
                return redirect("dogs:delete_account")

            # Удаляем пользователя (каскадное удаление сработает автоматически)
            user = request.user
            username = user.username
            user.delete()

            messages.success(
                request, f'Аккаунт пользователя "{username}" успешно удален.'
            )
            return redirect("dogs:landing_page")
    else:
        form = AccountDeletionForm()

    return render(
        request,
        "dogs/delete_account.html",
        {"form": form, "title": "Удаление аккаунта"},
    )


@login_required
def toggle_favorite(request, pk):
    """Добавление/удаление из избранного (AJAX)"""
    if request.method != "POST":
        return HttpResponseForbidden()

    try:
        is_favorite, message = toggle_favorite_for_user(request.user, pk)
    except Dog.DoesNotExist:
        return JsonResponse({"error": "Собака не найдена."}, status=404)
    except PermissionDenied:
        return HttpResponseForbidden()

    return JsonResponse({"is_favorite": is_favorite, "message": message})


@login_required
def matches_list(request):
    """Список мэтчей пользователя"""
    matches_qs = (
        Match.objects.filter(
            Q(dog_from__owner=request.user) | Q(dog_to__owner=request.user)
        )
        .select_related("dog_from", "dog_to", "dog_from__owner", "dog_to__owner")
        .order_by("-created_at")
    )

    paginator = Paginator(matches_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "dogs/matches.html",
        {
            "matches": page_obj.object_list,
            "page_obj": page_obj,
            "page_title": "Мои мэтчи",
        },
    )


@login_required
def favorites_list(request):
    """Список избранных собак"""
    favorites_qs = Favorite.objects.filter(user=request.user).select_related("dog")

    paginator = Paginator(favorites_qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "dogs/favorites.html",
        {
            "favorites": page_obj.object_list,
            "page_obj": page_obj,
            "page_title": "Избранное",
        },
    )


def about(request):
    """О сервисе"""
    return render(request, "dogs/about.html", {"page_title": "О сервисе"})


def breeds(request):
    """Породы"""
    return render(request, "dogs/breeds.html", {"page_title": "Породы собак"})


def events(request):
    """Мероприятия"""
    return render(request, "dogs/events.html", {"page_title": "Мероприятия"})


def tips(request):
    """Советы"""
    return render(request, "dogs/tips.html", {"page_title": "Полезные советы"})


def dog_profile(request, dog_id):
    """Профиль собаки (старый URL-адаптер)"""
    return dog_detail(request, dog_id)


# Error handlers
def handler404(request, exception):
    """Custom 404 error handler"""
    return render(
        request,
        "dogs/error_404.html",
        {
            "exception": exception,
            "request": request,
        },
        status=404,
    )


def handler500(request):
    """Custom 500 error handler"""
    from django.conf import settings

    return render(
        request,
        "dogs/error_500.html",
        {
            "request": request,
            "debug": settings.DEBUG,
        },
        status=500,
    )
