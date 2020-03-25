from django.contrib import admin
from .models import ArticleModel, CategoryModel, HospitalModel, ProvisionerModel, User

admin.site.site_header = "Pandemiia"


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
    list_display = ('name', 'category', 'status', 'count', 'units', 'last_edited_on')
    list_filter = ('status', 'category__name', 'units', 'created_on')
    search_fields = ['name',]

    fields = (('name', 'category'), ('count', 'units', 'status',),
              'hospital', 'author', 'attached_files', 'attached_image')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(ArticleAdmin, self).get_fieldsets(request, obj)

        if not request.user.is_superuser:
            remove_from_fieldsets(fieldsets, ('hospital', 'author', 'attached_files', 'attached_image'))
        return fieldsets

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(hospital=ProvisionerModel.objects.get(user=request.user).hospital)
        return qs

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'hospital', None) is None:
            obj.hospital = ProvisionerModel.objects.get(user=request.user).hospital
        obj.save()


class ArticleProvisionerInline(admin.TabularInline):
    model = ArticleModel
    exclude = ('attached_files', 'attached_image')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(ArticleProvisionerInline, self).get_fieldsets(request, obj)

        if not request.user.is_superuser:
            remove_from_fieldsets(fieldsets, ('hospital',))
        return fieldsets

    def save_formset(self, request, obj, form, change):
        if getattr(obj, 'hospital', None) is None:
            obj.hospital = ProvisionerModel.objects.get(user=request.user).hospital
        obj.save()


class ProvisionerAdmin(admin.ModelAdmin):
    fields = (("full_name", "hospital"),("tel", "email"))

    inlines = (ArticleProvisionerInline,)

    def get_queryset(self, request):
        qs = super(ProvisionerAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.hospital = ProvisionerModel.objects.get(user=request.user).hospital
            instance.save()
        formset.save_m2m()


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


class ArticleHospitalInline(admin.TabularInline):
    model = ArticleModel
    exclude = ('attached_files', 'attached_image')
    readonly_fields = ('category', 'name', 'count', 'units', 'status', 'author')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(ArticleHospitalInline, self).get_fieldsets(request, obj)

        if not request.user.is_superuser:
            remove_from_fieldsets(fieldsets, ('hospital',))
        return fieldsets

    def save_formset(self, request, obj, form, change):
        if getattr(obj, 'hospital', None) is None:
            obj.hospital = ProvisionerModel.objects.get(user=request.user).hospital
        obj.save()


class HospitalAdmin(admin.ModelAdmin):
    list_filter = ['region']

    inlines = [ArticleHospitalInline]



admin.site.register(ArticleModel, ArticleAdmin)
admin.site.register(ProvisionerModel, ProvisionerAdmin)
admin.site.register(CategoryModel, CategoryAdmin)
admin.site.register(HospitalModel, HospitalAdmin)
