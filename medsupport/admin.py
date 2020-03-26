from django.contrib import admin
from .models import ArticleModel, CategoryModel, HospitalModel, User
from .utils import remove_from_fieldsets

admin.site.site_header = "Pandemiia"


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
            return qs.filter(hospital=HospitalModel.objects.get(user=request.user))
        return qs

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'hospital', None) is None:
            obj.hospital = HospitalModel.objects.get(user=request.user)
        obj.save()


class ArticleHospitalInline(admin.TabularInline):
    model = ArticleModel
    exclude = ('attached_files', 'attached_image')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(ArticleHospitalInline, self).get_fieldsets(request, obj)

        if not request.user.is_superuser:
            remove_from_fieldsets(fieldsets, ('hospital',))
        return fieldsets

    def save_formset(self, request, obj, form, change):
        if getattr(obj, 'hospital', None) is None:
            obj.hospital = HospitalModel.objects.get(user=request.user)
        obj.save()


class HospitalAdmin(admin.ModelAdmin):
    fields = ('user', 'region', ("name", "contact_person"), ("tel", "email"))

    inlines = (ArticleHospitalInline,)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(HospitalAdmin, self).get_fieldsets(request, obj)

        if not request.user.is_superuser:
            remove_from_fieldsets(fieldsets, ('user',))
        return fieldsets

    def get_queryset(self, request):
        qs = super(HospitalAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.hospital = HospitalModel.objects.get(user=request.user)
            instance.save()
        formset.save_m2m()


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(ArticleModel, ArticleAdmin)
admin.site.register(CategoryModel, CategoryAdmin)
admin.site.register(HospitalModel, HospitalAdmin)
