from django.db import models
from django.contrib.auth.models import User


class Dog(models.Model):
    """Модель собаки"""
    GENDER_CHOICES = [
        ('M', 'Мальчик'),
        ('F', 'Девочка'),
    ]
    
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dogs',
        verbose_name='Владелец'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Кличка'
    )
    breed = models.CharField(
        max_length=100,
        verbose_name='Порода'
    )
    age = models.PositiveIntegerField(
        verbose_name='Возраст (в годах)'
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name='Пол'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    photo = models.ImageField(
        upload_to='dogs/',
        blank=True,
        null=True,
        verbose_name='Фото'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации'
    )

    class Meta:
        verbose_name = 'Собака'
        verbose_name_plural = 'Собаки'

    def __str__(self):
        return f"{self.name} ({self.breed})"