from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


ALLOWED_DOG_IMAGE_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_DOG_IMAGE_SIZE_MB = 5


def validate_dog_image(image):
    """Validate uploaded dog images for size and MIME type."""
    if not image:
        return

    size = getattr(image, "size", None)
    if size is not None and size > MAX_DOG_IMAGE_SIZE_MB * 1024 * 1024:
        raise ValidationError(
            _("Размер изображения не должен превышать %(size)s МБ."),
            params={"size": MAX_DOG_IMAGE_SIZE_MB},
        )

    content_type = getattr(image, "content_type", None)
    if content_type and content_type not in ALLOWED_DOG_IMAGE_MIME_TYPES:
        raise ValidationError(
            _("Допустимые форматы изображения: JPEG, PNG, WebP."),
        )


class Dog(models.Model):
    """Модель собаки"""

    GENDER_CHOICES = [
        ("M", "Мальчик"),
        ("F", "Девочка"),
    ]

    SIZE_CHOICES = [
        ("S", "Маленькая"),
        ("M", "Средняя"),
        ("L", "Большая"),
    ]

    LOOKING_FOR_CHOICES = [
        ("playmate", "Друга для игр"),
        ("companion", "Компаньона"),
        ("mate", "Партнера для жизни"),
        ("friendship", "Дружбы"),
    ]

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="dogs", verbose_name="Владелец"
    )
    name = models.CharField(max_length=100, verbose_name="Кличка")
    breed = models.CharField(max_length=100, verbose_name="Порода")
    age = models.PositiveIntegerField(
        verbose_name="Возраст (в годах)",
        validators=[MinValueValidator(0), MaxValueValidator(20)],
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, verbose_name="Размер")
    temperament = models.CharField(
        max_length=100,
        verbose_name="Характер",
        help_text="Например: дружелюбный, энергичный, спокойный",
    )
    looking_for = models.CharField(
        max_length=20,
        choices=LOOKING_FOR_CHOICES,
        verbose_name="Ищет",
        help_text="Цель знакомства",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Расскажите о вашей собаке: привычки, любимые занятия и т.д.",
    )
    photo = models.ImageField(
        upload_to="dogs/",
        blank=True,
        null=True,
        verbose_name="Фото",
        validators=[validate_dog_image],
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активный профиль")

    class Meta:
        verbose_name = "Собака"
        verbose_name_plural = "Собаки"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"],
                name="unique_dog_name_per_owner",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.owner.username})"


class UserProfile(models.Model):
    """Расширенная модель пользователя"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Пользователь",
    )
    bio = models.TextField(blank=True, verbose_name="О себе")
    location = models.CharField(max_length=100, blank=True, verbose_name="Город")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="Аватар"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"Профиль {self.user.username}"


class Match(models.Model):
    """Модель для хранения мэтчей собак"""

    STATUS_CHOICES = [
        ("pending", "Ожидает"),
        ("accepted", "Принят"),
        ("declined", "Отклонен"),
    ]

    dog_from = models.ForeignKey(
        Dog,
        on_delete=models.CASCADE,
        related_name="matches_sent",
        verbose_name="Собака-инициатор",
    )
    dog_to = models.ForeignKey(
        Dog,
        on_delete=models.CASCADE,
        related_name="matches_received",
        verbose_name="Собака-цель",
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending", verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Мэтч"
        verbose_name_plural = "Мэтчи"
        constraints = [
            models.UniqueConstraint(
                fields=["dog_from", "dog_to"],
                name="unique_match_dog_from_dog_to",
            ),
        ]
        indexes = [
            models.Index(fields=["dog_from"], name="idx_match_dog_from"),
            models.Index(fields=["dog_to"], name="idx_match_dog_to"),
            models.Index(
                fields=["dog_from", "dog_to"],
                name="idx_match_dog_from_dog_to",
            ),
        ]

    def __str__(self):
        return (
            f"{self.dog_from.name} ({self.dog_from.owner.username}) "
            f"→ {self.dog_to.name} ({self.dog_to.owner.username}): "
            f"{self.get_status_display()}"
        )


class Message(models.Model):
    """Модель для сообщений между пользователями"""

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages_sent",
        verbose_name="Отправитель",
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages_received",
        verbose_name="Получатель",
    )
    subject = models.CharField(max_length=200, verbose_name="Тема")
    content = models.TextField(verbose_name="Содержание")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["-created_at"]

    def __str__(self):
        return f"От {self.sender.username} к {self.receiver.username}: {self.subject}"


class Favorite(models.Model):
    """Модель для избранных собак"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite_dogs",
        verbose_name="Пользователь",
    )
    dog = models.ForeignKey(
        Dog,
        on_delete=models.CASCADE,
        related_name="favorited_by",
        verbose_name="Собака",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "dog"],
                name="unique_favorite_per_user_and_dog",
            ),
        ]
        indexes = [
            models.Index(fields=["user"], name="idx_favorite_user"),
            models.Index(fields=["dog"], name="idx_favorite_dog"),
            models.Index(fields=["user", "dog"], name="idx_favorite_user_dog"),
        ]

    def __str__(self):
        return f"{self.user.username} добавил в избранное {self.dog.name}"
