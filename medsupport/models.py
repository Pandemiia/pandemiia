from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .choises import STATUS, UNITS, REGION


class CategoryPointModel(models.Model):
    name = models.CharField("Категорія закладів", max_length=400)

    class Meta:
        verbose_name = "Категорія закладів"
        verbose_name_plural = "Категорії закладів"

    def __str__(self):
        return self.name


class CategoryArticleModel(models.Model):
    name = models.CharField("Категорія товару", max_length=400)

    class Meta:
        verbose_name = "Категорія товарів"
        verbose_name_plural = "Категорії товарів"

    def __str__(self):
        return self.name


class PointModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField("Назва медзакладу", max_length=400)
    description = models.CharField("Опис", max_length=1000, blank=True)
    category = models.ManyToManyField(CategoryPointModel)

    # Address data
    region = models.IntegerField("Область", choices=REGION, default=0)
    city = models.CharField('Місто', max_length=50)
    zip_code = models.CharField('Поштовий індекс', max_length=50)
    line1 = models.CharField('Повний адрес', max_length=50)
    geo_lat = models.IntegerField("Геопозиція: широта", blank=True, null=True)
    geo_lng = models.IntegerField("Геопозиція: довгота", blank=True, null=True)

    class Meta:
        verbose_name = "Госпіталь"
        verbose_name_plural = "Госпіталі"

    def __str__(self):
        if self.name:
            return self.name
        return self.user.username


class PointContactPersonModel(models.Model):
    point = models.ForeignKey(PointModel, on_delete=models.CASCADE)
    full_name = models.CharField("ПІБ контактної особи", max_length=200, blank=True)
    position = models.CharField("Посада", max_length=200, blank=True)
    email = models.EmailField("Email", blank=True)
    tel = models.CharField("Контактний телефон", max_length=13, blank=True)

    class Meta:
        verbose_name = "Контактна особа"
        verbose_name_plural = "Контактні особи"

    def __str__(self):
        return self.full_name


class PhoneContactPersonModel(models.Model):
    tel = models.CharField("Контактний телефон", max_length=13, blank=True)
    contact_person = models.ForeignKey(PointContactPersonModel, on_delete=models.CASCADE)


# Auto create and auto edit object of PointModel with User
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        PointModel.objects.create(user=instance)
    instance.pointmodel.save()


class ArticleModel(models.Model):
    category = models.ManyToManyField(CategoryArticleModel, verbose_name="Категорії")
    name = models.CharField("Назва товару", max_length=200)
    description = models.CharField("Опис", max_length=1000)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        return self.name


class NeedModel(models.Model):
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE)
    point = models.ForeignKey(PointModel, verbose_name="Лікарня", on_delete=models.CASCADE)
    quantity_needed = models.IntegerField("Скільки ще потрібно", default=0)
    quantity_done = models.IntegerField("Скільки вже отримано", default=0)
    units = models.IntegerField("Одиниці вимірювання", choices=UNITS, default=0)
    status = models.IntegerField("Статус", choices=STATUS, default=0)
    created_on = models.DateTimeField("Дата створення", auto_now_add=True, blank=True, null=True)
    last_edited_on = models.DateTimeField("Востаннє відредаговано", auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "Потреба"
        verbose_name_plural = "Потреби"

    def __str__(self):
        return self.article.name

