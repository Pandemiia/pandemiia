# Generated by Django 3.0.4 on 2020-05-04 16:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('medsupport', '0012_solution_approved_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(blank=True, max_length=13, validators=[django.core.validators.RegexValidator(message='Телефонний номер має бути в форматі +380123456789', regex='^\\+?3?8?(0\\d{9})$')], verbose_name='Контактний телефон'),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Логін користувача'),
        ),
    ]
