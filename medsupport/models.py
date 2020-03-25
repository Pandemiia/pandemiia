from django.db import models

UNITS = (
    (0, 'шт'),
    (1, 'уп'),
    (2, 'фл'),
)

STATUS = (
    (0, 'Є потреба'),
    (1, 'Отримано'),
)


class HospitalModel(models.Model):
    name = models.CharField("Назва медзакладу", max_length=400)
    city = models.CharField("Місто/населений пункт", max_length=200)

    class Meta:
        verbose_name = "Госпіталь"
        verbose_name_plural = "Госпіталі"

    def __str__(self):
        return self.name


class CategoryModel(models.Model):
    name = models.CharField("Категорія товару", max_length=400)

    class Meta:
        verbose_name = "Категорія товарів"
        verbose_name_plural = "Категорії товарів"

    def __str__(self):
        return self.name


class ArticleModel(models.Model):
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    name = models.CharField("Назва товару", max_length=400)
    units = models.IntegerField("Одиниці вимірювання", choices=UNITS, default=0)
    count = models.IntegerField("Кількість")
    status = models.IntegerField("Статус", choices=STATUS, default=0)
    hospital = models.ForeignKey(HospitalModel, on_delete=models.CASCADE)
    created_on = models.DateTimeField("Дата створення", auto_now_add=True)
    last_edited_on = models.DateTimeField("Востаннє відредаговано", auto_now=True)
    attached_image = models.ImageField("Прикріплене зображення", upload_to='articles/image_files',
                                       null=True, blank=True)
    attached_files = models.FileField("Прикріплені файли", upload_to='articles/attached_files',
                                      null=True, blank=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        return self.name
