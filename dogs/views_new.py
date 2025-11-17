# Дополнительные views для menu приложения
from django.shortcuts import render


def contacts(request):
    """Контакты"""
    return render(request, "dogs/contacts.html", {"page_title": "Контакты"})


def privacy(request):
    """Политика конфиденциальности"""
    return render(
        request, "dogs/privacy.html", {"page_title": "Политика конфиденциальности"}
    )
