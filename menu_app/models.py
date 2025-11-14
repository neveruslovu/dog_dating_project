from django.db import models
from django.urls import reverse


class Menu(models.Model):
    """Модель для хранения меню"""
    name = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name='Название меню'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Модель для хранения пунктов меню"""
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Меню'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительский пункт'
    )
    title = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    url = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='URL'
    )
    named_url = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Named URL'
    )
    order = models.IntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title

    def get_url(self):
        """Получить URL пункта меню"""
        if self.named_url:
            try:
                return reverse(self.named_url)
            except:
                pass
        return self.url or '#'

    def save(self, *args, **kwargs):
        """Валидация: должен быть указан либо url, либо named_url"""
        if not self.url and not self.named_url:
            self.url = '#'
        super().save(*args, **kwargs)from django.db import models
from django.urls import reverse


class Menu(models.Model):
    """Модель для хранения меню"""
    name = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name='Название меню'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Модель для хранения пунктов меню"""
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Меню'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительский пункт'
    )
    title = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    url = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='URL'
    )
    named_url = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Named URL'
    )
    order = models.IntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title

    def get_url(self):
        """Получить URL пункта меню"""
        if self.named_url:
            try:
                return reverse(self.named_url)
            except:
                pass
        return self.url or '#'

    def save(self, *args, **kwargs):
        """Валидация: должен быть указан либо url, либо named_url"""
        if not self.url and not self.named_url:
            self.url = '#'
        super().save(*args, **kwargs)