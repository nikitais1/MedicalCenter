from django.conf import settings
from django.db import models

# Create your models here.
NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    """Модель категории."""
    category_title = models.CharField(max_length=100, verbose_name='название')
    category_description = models.TextField(verbose_name='описание')
    category_image = models.ImageField(upload_to='categories/', verbose_name='изображение', **NULLABLE)

    def __str__(self):
        return self.category_title

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Service(models.Model):
    """Модель услуги."""
    services_title = models.CharField(max_length=100, verbose_name='название')
    services_description = models.TextField(verbose_name='описание')
    price = models.PositiveIntegerField(verbose_name='цена')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='категория')
    deadline = models.CharField(max_length=100, verbose_name='срок выполнения')

    def __str__(self):
        return self.services_title

    class Meta:
        verbose_name = "услуга"
        verbose_name_plural = "услуги"


class Cart(models.Model):
    """Модель корзины."""
    client = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='клиент')
    services = models.ManyToManyField('Service', verbose_name='услуги')
    date = models.DateTimeField(verbose_name='дата и время', **NULLABLE)

    def __str__(self):
        return f'{self.client} - {self.services}'

    class Meta:
        verbose_name = "корзина"
        verbose_name_plural = "корзины"
