from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Dog, UserProfile, Match, Favorite


class UserRegistrationForm(UserCreationForm):
    """Форма регистрации нового пользователя"""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "your@email.com"}
        ),
        label="Email",
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "username"}
        ),
        label="Имя пользователя",
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "••••••••"}
        ),
        label="Пароль",
        help_text="Пароль должен содержать минимум 8 символов",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "••••••••"}
        ),
        label="Подтверждение пароля",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем стандартные help_texts
        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # Создаем UserProfile автоматически
            try:
                UserProfile.objects.create(user=user)
            except:
                pass  # If creation fails, continue
        return user


class UserLoginForm(AuthenticationForm):
    """Форма входа пользователя"""

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Имя пользователя или email"}
        ),
        label="Имя пользователя или Email",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "••••••••"}
        ),
        label="Пароль",
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Запомнить меня",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Имя пользователя или Email"


class DogForm(forms.ModelForm):
    """Форма для создания/редактирования профиля собаки"""

    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control", "accept": "image/*"}),
        label="Фото",
        help_text="Рекомендуемый размер: 400x400 пикселей",
    )

    class Meta:
        model = Dog
        fields = [
            "name",
            "breed",
            "age",
            "gender",
            "size",
            "temperament",
            "looking_for",
            "description",
            "photo",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Кличка собаки"}
            ),
            "breed": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Лабрадор, Такса, Спаниель и т.д.",
                }
            ),
            "age": forms.NumberInput(
                attrs={"class": "form-control", "min": "0", "max": "25"}
            ),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "size": forms.Select(attrs={"class": "form-select"}),
            "temperament": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Дружелюбный, энергичный, спокойный...",
                }
            ),
            "looking_for": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "4",
                    "placeholder": "Расскажите о вашей собаке: привычки, любимые занятия, характер...",
                }
            ),
        }
        labels = {
            "name": "Кличка",
            "breed": "Порода",
            "age": "Возраст (лет)",
            "gender": "Пол",
            "size": "Размер",
            "temperament": "Характер",
            "looking_for": "Ищу",
            "description": "Описание",
            "photo": "Фото",
        }
        help_texts = {
            "temperament": "Опишите характер вашей собаки",
            "looking_for": "Цель знакомства",
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Если это новая собака, скрываем владельца (автоматически текущий пользователь)
        if not self.instance.pk and self.user:
            # Устанавливаем владельца автоматически
            self.instance.owner = self.user
            # Скрываем поле owner из формы только если оно существует
            if "owner" in self.fields:
                del self.fields["owner"]

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age is not None and (age < 0 or age > 20):
            raise ValidationError("Возраст должен быть от 0 до 20 лет")
        return age

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")
        if not photo:
            return photo

        max_mb = 5
        if getattr(photo, "size", 0) > max_mb * 1024 * 1024:
            raise ValidationError(f"Размер изображения не должен превышать {max_mb} МБ")

        content_type = getattr(photo, "content_type", "")
        if content_type not in {"image/jpeg", "image/png", "image/webp"}:
            raise ValidationError("Допустимые форматы изображения: JPEG, PNG, WebP")

        return photo


class UserProfileForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя"""

    class Meta:
        model = UserProfile
        fields = ["bio", "location", "phone", "avatar"]
        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "3",
                    "placeholder": "Расскажите о себе...",
                }
            ),
            "location": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Город"}
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+7 (123) 456-78-90",
                    "type": "tel",
                }
            ),
            "avatar": forms.FileInput(
                attrs={"class": "form-control", "accept": "image/*"}
            ),
        }
        labels = {
            "bio": "О себе",
            "location": "Город",
            "phone": "Телефон",
            "avatar": "Аватар",
        }


class PasswordChangeForm(forms.Form):
    """Форма для изменения пароля"""

    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "••••••••"}
        ),
        label="Текущий пароль",
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "••••••••"}
        ),
        label="Новый пароль",
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "••••••••"}
        ),
        label="Подтверждение нового пароля",
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 != new_password2:
            raise ValidationError("Пароли не совпадают")

        return cleaned_data


class AccountDeletionForm(forms.Form):
    """Форма для удаления аккаунта"""

    confirm_deletion = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Я подтверждаю удаление аккаунта и понимаю, что это действие нельзя отменить",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "••••••••"}
        ),
        label="Подтвердите пароль",
    )


class DogSearchForm(forms.Form):
    """Форма поиска собак"""

    breed = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Порода собаки"}
        ),
        label="Порода",
    )
    age_min = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "От",
                "min": "0",
                "max": "25",
            }
        ),
        label="Возраст от",
    )
    age_max = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "До",
                "min": "0",
                "max": "25",
            }
        ),
        label="Возраст до",
    )
    gender = forms.ChoiceField(
        required=False,
        choices=[("", "Любой")] + list(Dog.GENDER_CHOICES),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Пол",
    )
    size = forms.ChoiceField(
        required=False,
        choices=[("", "Любой")] + list(Dog.SIZE_CHOICES),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Размер",
    )


class MatchForm(forms.ModelForm):
    """Форма для создания/редактирования мэтча между собаками."""

    class Meta:
        model = Match
        fields = ["dog_from", "dog_to"]

    def clean(self):
        cleaned_data = super().clean()
        dog_from = cleaned_data.get("dog_from")
        dog_to = cleaned_data.get("dog_to")

        if dog_from and dog_to and dog_from == dog_to:
            raise ValidationError("Нельзя создать мэтч для одной и той же собаки.")

        return cleaned_data


class FavoriteForm(forms.ModelForm):
    """Форма для добавления собаки в избранное."""

    class Meta:
        model = Favorite
        fields = ["user", "dog"]

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get("user")
        dog = cleaned_data.get("dog")

        if user and dog and dog.owner == user:
            raise ValidationError("Нельзя добавлять собственную собаку в избранное.")

        return cleaned_data
