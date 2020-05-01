from django.db import models
from django.core.validators import RegexValidator
from django.db.models import Sum

from users.models import User
from .choices import REGION_CHOICES, NEED_UNITS


class HospitalCategory(models.Model):
    name = models.CharField("Категорія закладів", max_length=400)

    class Meta:
        verbose_name = "Категорія закладів"
        verbose_name_plural = "Категорії закладів"

    def __str__(self):
        return self.name


class Hospital(models.Model):
    users = models.ManyToManyField(User, verbose_name="Логін користувача")
    name = models.CharField("Назва медзакладу", max_length=400)
    description = models.CharField("Опис", max_length=1000, blank=True)
    categories = models.ManyToManyField(HospitalCategory)

    # Address data
    region = models.IntegerField("Область", choices=REGION_CHOICES)
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
        ordering = ['pk']

    def __str__(self):
        if self.name:
            return self.name
        return str(self.pk)

    @property
    def need_types(self):
        # TODO: refactor to avoid multiple queries on list
        return SolutionType.objects.filter(
            hospital_needs__hospital=self
        ).annotate(
            received=Sum('hospital_needs__quantity_received'),
            needed=Sum('hospital_needs__quantity_needed')
        )


class Contact(models.Model):
    hospital = models.ForeignKey(Hospital, related_name='contacts', on_delete=models.CASCADE)
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


class SolutionCategory(models.Model):
    name = models.CharField("Категорія рішень", max_length=400)

    class Meta:
        verbose_name = "Категорія рішень"
        verbose_name_plural = "Категорії рішень"

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField("Назва матеріалу", max_length=200)

    class Meta:
        verbose_name = "Матеріал"
        verbose_name_plural = "Матеріали"

    def __str__(self):
        return self.name


class Tool(models.Model):
    name = models.CharField("Назва інструменту", max_length=200)

    class Meta:
        verbose_name = "Засіб"
        verbose_name_plural = "Засоби"

    def __str__(self):
        return self.name


class SolutionType(models.Model):
    name = models.CharField("Назва типу товару товару", max_length=200)
    units = models.CharField(
        "Одиниці вимірювання",
        choices=NEED_UNITS,
        default=NEED_UNITS.pieces,
        max_length=255,
    )

    class Meta:
        verbose_name = "Тип засобу"
        verbose_name_plural = "Тип засобів"

    def __str__(self):
        return self.name


class Solution(models.Model):
    solution_type = models.ForeignKey(
        SolutionType,
        verbose_name="Тип рішення",
        related_name='solutions',
        blank=True, null=True,
        on_delete=models.CASCADE,
    )
    categories = models.ManyToManyField(SolutionCategory, verbose_name="Категорії")
    name = models.CharField("Назва товару", max_length=200)
    code = models.CharField("Код товару", max_length=10, default="-")
    need_description = models.TextField("Опис потреби", max_length=1000)
    definition = models.TextField("Визначення", max_length=1000)
    main_image = models.ImageField("Головне зображення", upload_to="solution_images")
    # attachment = models.FileField("Архів з файлами", upload_to="solution_attachment")
    attachment = models.URLField("Посилання на завантаження архіву", max_length=200, blank=True)
    instruction = models.TextField("Варіанти виготовлення", max_length=1000)
    materials = models.ManyToManyField(Material, verbose_name="Матеріали, з яких можна виготовляти")
    tools = models.ManyToManyField(Tool, verbose_name="Засоби для виготовлення")
    approved_by = models.CharField("Ким затверджено", max_length=200, blank=True)
    source = models.URLField("Джерело", blank=True)

    class Meta:
        verbose_name = "Рішення"
        verbose_name_plural = "Рішення"

    def __str__(self):
        return self.name


class SolutionImage(models.Model):
    image = models.ImageField("Фото рішення", upload_to="solution_images")
    solution = models.ForeignKey(
        Solution,
        related_name='images',
        verbose_name="Рішення",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"

    def __str__(self):
        return f"{self.solution.name} | id: {self.id}"


class HospitalNeed(models.Model):
    solution_type = models.ForeignKey(
        SolutionType,
        related_name='hospital_needs',
        verbose_name="Тип рішення",
        on_delete=models.CASCADE,
    )
    hospital = models.ForeignKey(
        Hospital,
        related_name='needs',
        verbose_name="Лікарня",
        on_delete=models.CASCADE,
    )
    quantity_needed = models.PositiveIntegerField("Скільки ще потрібно", default=0)
    quantity_received = models.PositiveIntegerField("Скільки вже отримано", default=0)
    created = models.DateTimeField("Дата створення", auto_now_add=True, blank=True, null=True)
    edited = models.DateTimeField("Востаннє відредаговано", auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "Потреба"
        verbose_name_plural = "Потреби"

    def __str__(self):
        return self.solution_type.name

