from django.contrib import admin
from .models import ArticleModel, CategoryModel, HospitalModel


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'hospital', 'status', 'count', 'units', 'last_edited_on')
    list_filter = ('status', 'category', 'units', 'created_on')
    search_fields = ['name']


admin.site.register(ArticleModel, ArticleAdmin)
admin.site.register(CategoryModel)
admin.site.register(HospitalModel)
