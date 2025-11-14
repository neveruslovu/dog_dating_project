from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Dog


def home(request):
    """Главная страница"""
    return render(request, 'dogs/home.html')


@login_required
def register_dog(request):
    """Регистрация собаки"""
    if request.method == 'POST':
        # Обработка формы
        pass
    return render(request, 'dogs/register.html')


@login_required
def dog_profile(request, dog_id):
    """Профиль собаки"""
    dog = Dog.objects.get(id=dog_id)
    return render(request, 'dogs/profile.html', {'dog': dog})


@login_required
def matches(request):
    """Страница подбора пар"""
    dogs = Dog.objects.exclude(owner=request.user)
    return render(request, 'dogs/matches.html', {'dogs': dogs})


def about(request):
    """О сервисе"""
    return render(request, 'dogs/about.html')


def breeds(request):
    """Породы"""
    return render(request, 'dogs/breeds.html')


def events(request):
    """Мероприятия"""
    return render(request, 'dogs/events.html')


def tips(request):
    """Советы"""
    return render(request, 'dogs/tips.html')