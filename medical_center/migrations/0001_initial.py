# Generated by Django 5.0.6 on 2024-05-26 11:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_title', models.CharField(max_length=100, verbose_name='название')),
                ('category_description', models.TextField(verbose_name='описание')),
                ('category_image', models.ImageField(blank=True, null=True, upload_to='categories/', verbose_name='изображение')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('services_title', models.CharField(max_length=100, verbose_name='название')),
                ('services_description', models.TextField(verbose_name='описание')),
                ('price', models.PositiveIntegerField(verbose_name='цена')),
                ('deadline', models.CharField(max_length=100, verbose_name='срок выполнения')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical_center.category', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'услуга',
                'verbose_name_plural': 'услуги',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True, verbose_name='дата и время')),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='клиент')),
                ('services', models.ManyToManyField(to='medical_center.service', verbose_name='услуги')),
            ],
            options={
                'verbose_name': 'корзина',
                'verbose_name_plural': 'корзины',
            },
        ),
    ]
