from django.contrib import admin
from .models import ArticleModel, CategoryModel, HospitalModel, HospitalNeedModel
from .utils import remove_from_fieldsets

admin.site.site_header = "Pandemiia"


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category__name',)
    search_fields = ['name',]

    fields = (('name', 'category'),
              'attached_files', 'attached_image')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(ArticleAdmin, self).get_fieldsets(request, obj)

        if not request.user.is_superuser:
            remove_from_fieldsets(fieldsets, ('attached_files', 'attached_image'))
        return fieldsets


class ArticleHospitalInline(admin.TabularInline):
    model = ArticleModel
    exclude = ('attached_files', 'attached_image')


class HospitalNeedAdmin(admin.ModelAdmin):
    fields = (('article', 'status'), ('count', 'units'), 'hospital')

    # inlines = (ArticleHospitalInline,)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(HospitalNeedAdmin, self).get_fieldsets(request, obj)

        if not request.user.is_superuser:
            remove_from_fieldsets(fieldsets, ('hospital',))
        return fieldsets

    def get_queryset(self, request):
        qs = super(HospitalNeedAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(hospital=HospitalModel.objects.get(user=request.user))
        return qs

    def save_formset(self, request, obj, form, change):
        if getattr(obj, 'hospital', None) is None:
            obj.hospital = HospitalModel.objects.get(user=request.user)
        obj.save()


class HospitalNeedInlineAdmin(admin.TabularInline):
    model = HospitalNeedModel
    fields = ('article', 'count', 'units', 'status', 'hospital')
    autocomplete_fields = ['article']
    inlines = (ArticleHospitalInline,)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(HospitalNeedInlineAdmin, self).get_fieldsets(request, obj)

        if not request.user.is_superuser:
            remove_from_fieldsets(fieldsets, ('hospital',))
        return fieldsets

    def get_queryset(self, request):
        qs = super(HospitalNeedInlineAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(hospital=HospitalModel.objects.get(user=request.user))
        return qs

    def save_formset(self, request, obj, form, change):
        if getattr(obj, 'hospital', None) is None:
            obj.hospital = HospitalModel.objects.get(user=request.user)
        obj.save()



class HospitalAdmin(admin.ModelAdmin):
    fields = ('user', 'region', ("name", "contact_person"), ("tel", "email"))

    inlines = (HospitalNeedInlineAdmin,)

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
admin.site.register(HospitalNeedModel, HospitalNeedAdmin)
admin.site.register(HospitalModel, HospitalAdmin)
