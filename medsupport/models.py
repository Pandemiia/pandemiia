from django.db import models
from django.core.validators import RegexValidator

from users.models import User
from .choices import REGION, NEED_UNITS


class HospitalCategory(models.Model):
    name = models.CharField("Категорія закладів", max_length=400)

    class Meta:
        verbose_name = "Категорія закладів"
        verbose_name_plural = "Категорії закладів"

    def __str__(self):
        return self.name


class Hospital(models.Model):
    user = models.ManyToManyField(User, verbose_name="Логін користувача")
    name = models.CharField("Назва медзакладу", max_length=400)
    description = models.CharField("Опис", max_length=1000, blank=True)
    categories = models.ManyToManyField(HospitalCategory)

    # Address data
    region = models.IntegerField("Область", choices=REGION, default=0)
    city = models.CharField('Місто', max_length=50)
    zip_code_validator = RegexValidator(regex="^\\d{5}$", message="Поштовий індекс має бути в форматі 01234")
    zip_code = models.CharField('Поштовий індекс', max_length=50, validators=[zip_code_validator], blank=True)
    line1 = models.CharField('Повний адрес', max_length=100)
    company_code = models.IntegerField("Код ЄДРПОУ", null=True, blank=True)
    email = models.EmailField("Електронна адреса установи", blank=True)
    geo_lat = models.CharField("Геопозиція: широта (lat)", max_length=50, blank=True, null=True)
    geo_lng = models.CharField("Геопозиція: довгота (lng)", max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Медичний заклад"
        verbose_name_plural = "Медичні заклади"

    def __str__(self):
        if self.name:
            return self.name
        return str(self.pk)


class Contact(models.Model):
    hospital = models.ForeignKey(Hospital, related_name='hospitals', on_delete=models.CASCADE)
    full_name = models.CharField("ПІБ контактної особи", max_length=200, blank=True)
    position = models.CharField("Посада", max_length=200, blank=True)
    email = models.EmailField("Email", unique=True, blank=True)
    phone = models.CharField(
        "Контактний телефон",
        max_length=13,
        validators=[RegexValidator(
            regex=r'^\+?3?8?(0\d{9})$',
            message="Телефонний номер має бути в форматі +380123456789"
        )],
        unique=True,
        blank=True
    )

    class Meta:
        verbose_name = "Контактна особа"
        verbose_name_plural = "Контактні особи"

    def __str__(self):
        return self.full_name


class PhoneContactPerson(models.Model):
    tel = models.CharField("Контактний телефон", max_length=13, blank=True)
    contact_person = models.ForeignKey(Contact, on_delete=models.CASCADE)


class SolutionCategory(models.Model):
    name = models.CharField("Категорія рішень", max_length=400)

    class Meta:
        verbose_name = "Категорія рішень"
        verbose_name_plural = "Категорії рішень"

    def __str__(self):
        return self.name


class Solution(models.Model):
    categories = models.ManyToManyField(SolutionCategory, verbose_name="Категорії")
    name = models.CharField("Назва товару", max_length=200)
    description = models.CharField("Опис", max_length=1000)
    main_image = models.ImageField("Головне зображення", upload_to="article_images", blank=True)
    attachment = models.FileField("Прикріплений файл", upload_to="article_attachment", blank=True)
    instruction = models.TextField("Інструкція", max_length=1000, blank=True)
    materials = models.CharField("Матеріали, з яких можна виготовляти", max_length=200, blank=True)
    tools = models.CharField("Засоби для виготовлення", max_length=200, blank=True)
    approved_by = models.CharField("Ким затверджено", max_length=200, blank=True)

    class Meta:
        verbose_name = "Рішення"
        verbose_name_plural = "Рішення"

    def __str__(self):
        return self.name


class HospitalNeed(models.Model):
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, verbose_name="Лікарня", on_delete=models.CASCADE)
    quantity_needed = models.PositiveIntegerField("Скільки ще потрібно", default=0)
    quantity_received = models.PositiveIntegerField("Скільки вже отримано", default=0)
    units = models.CharField(
        "Одиниці вимірювання",
        choices=NEED_UNITS,
        default=NEED_UNITS.pieces,
        max_length=255,
    )
    created = models.DateTimeField("Дата створення", auto_now_add=True, blank=True, null=True)
    edited = models.DateTimeField("Востаннє відредаговано", auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "Потреба"
        verbose_name_plural = "Потреби"

    def __str__(self):
        return self.solution.name

