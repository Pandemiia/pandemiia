from django.contrib import admin
from .models import ArticleModel, CategoryModel, HospitalModel


# Remove field from fieldsets
def remove_from_fieldsets(fieldsets, fields):
    for fieldset in fieldsets:
        for field in fields:
            if field in fieldset[1]['fields']:
                new_fields = []
                for new_field in fieldset[1]['fields']:
                    if not new_field in fields:
                        new_fields.append(new_field)

                fieldset[1]['fields'] = tuple(new_fields)
                break


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'hospital', 'status', 'count', 'units', 'last_edited_on')
    list_filter = ('status', 'category__name', 'hospital__name', 'units', 'created_on')
    search_fields = ['name']

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(ArticleAdmin, self).get_fieldsets(request, obj)

        if not request.user.is_superuser:
            remove_from_fieldsets(fieldsets, ('hospital',))
        return fieldsets

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'hospital', None) is None:
            obj.author = request.user
        obj.save()


admin.site.register(ArticleModel, ArticleAdmin)
admin.site.register(CategoryModel)
admin.site.register(HospitalModel)
