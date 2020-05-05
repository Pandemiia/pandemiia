from django.contrib import admin
from .models import (
    Hospital,  Contact,
    HospitalCategory, SolutionCategory,
    Solution, HospitalNeed,
    SolutionImage, Tool,
    Material, SolutionType,
    ApprovedBy
)


class NeedInline(admin.TabularInline):
    model = HospitalNeed
    fields = ('solution_type', ('quantity_needed', 'quantity_received'),)
    autocomplete_fields = ['solution_type']
    extra = 1


class ContactInline(admin.TabularInline):
    model = Contact
    classes = ('collapse',)
    fields = ('hospital', 'full_name', 'position', 'phone', 'email')
    extra = 0


class SolutionImageInline(admin.TabularInline):
    verbose_name_plural = "Додаткові фото"
    model = SolutionImage
    extra = 1


@admin.register(SolutionCategory)
class SolutionCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    pass


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    pass


@admin.register(ApprovedBy)
class ApprovedByAdmin(admin.ModelAdmin):
    pass


@admin.register(SolutionType)
class SolutionTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    filter_horizontal = ('categories',)


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'solution_type', 'code', 'approved_by')
    fieldsets = (
        (None, {
            'fields': (('code', 'name'), 'solution_type', 'need_description', 'definition')
        }),
        (None, {
            'fields': (('main_image', 'attachment'), 'instruction')
        }),
        ("Матеріали та засоби", {
            'classes': ('collapse',),
            'fields': ('materials', 'tools')
        }),
        ("Затвердження", {
            'fields': (('approved_by', 'comment'),)
        })

    )
    search_fields = ('name',)
    filter_horizontal = ('materials', 'tools')
    inlines = (SolutionImageInline,)


@admin.register(HospitalNeed)
class NeedAdmin(admin.ModelAdmin):
    pass


@admin.register(HospitalCategory)
class HospitalCategoryAdmin(admin.ModelAdmin):
    fields = ('name',)


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Користувачі", {
            'classes': ('collapse',),
            'fields': ('users',)
        }),
        (None, {
            'fields': (('name', 'description'))
        }),
        ("Категорія установи", {
            'classes': ('collapse',),
            'fields': ('categories',)
        }),
        ("Адрес", {
            'classes': ('collapse',),
            'fields': (('region', 'city'), ('line1', 'zip_code'), ('geo_lat', 'geo_lng'))
        }),
        ("Додатково", {
            'classes': ('collapse',),
            'fields': (('company_code'), ('email'))
        }),
    )
    filter_horizontal = ('users','categories',)
    inlines = (ContactInline, NeedInline)

    def get_queryset(self, request):
        qs = super(HospitalAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs

    def get_readonly_fields(self, request, obj=None):
        fields = list(super(HospitalAdmin, self).get_readonly_fields(request, obj))

        # add User field to read_only if user is not superuser
        if not request.user.is_superuser:
            fields.append('user')
        return fields
