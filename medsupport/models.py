from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .choises import STATUS, UNITS, REGION


class HospitalModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField("Назва медзакладу", max_length=400)
    region = models.IntegerField("Область", choices=REGION, default=0)
    contact_person = models.CharField("ПІБ контактної особи", max_length=200, blank=True)
    email = models.EmailField("Email", blank=True)
    tel = models.CharField("Контактний телефон", max_length=13, blank=True)


    class Meta:
        verbose_name = "Госпіталь"
        verbose_name_plural = "Госпіталі"

    def __str__(self):
        return self.name


# Autocreate and autoedit provisioner model with User
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        HospitalModel.objects.create(user=instance)
    instance.hospitalmodel.save()


class CategoryModel(models.Model):
    name = models.CharField("Категорія товару", max_length=400)

    class Meta:
        verbose_name = "Категорія товарів"
        verbose_name_plural = "Категорії товарів"

    def __str__(self):
        return self.name


class ArticleModel(models.Model):
    category = models.ForeignKey(CategoryModel, verbose_name="Категорія", on_delete=models.CASCADE)
    name = models.CharField("Назва товару", max_length=400)

    attached_image = models.ImageField("Прикріплене зображення", upload_to='articles/image_files',
                                       null=True, blank=True)
    attached_files = models.FileField("Прикріплені файли", upload_to='articles/attached_files',
                                      null=True, blank=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        return self.name


class HospitalNeedModel(models.Model):
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE)
    count = models.IntegerField("Кількість")
    units = models.IntegerField("Одиниці вимірювання", choices=UNITS, default=0)
    hospital = models.ForeignKey(HospitalModel, verbose_name="Лікарня", on_delete=models.CASCADE)
    status = models.IntegerField("Статус", choices=STATUS, default=0)
    created_on = models.DateTimeField("Дата створення", auto_now_add=True, blank=True, null=True)
    last_edited_on = models.DateTimeField("Востаннє відредаговано", auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "Потреба"
        verbose_name_plural = "Потреби"

    def __str__(self):
        return self.article.name
