from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.db import models

# Create your models here.
NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """Модель пользователя."""
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')

    birth_date = models.DateField(verbose_name='Дата рождения', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    verify_code = models.CharField(max_length=12, blank=True, null=True)
    email_confirmation_token = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.email_confirmation_token:
            self.email_confirmation_token = default_token_generator.make_token(self)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
