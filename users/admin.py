from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import ugettext_lazy as _

from allauth.account.models import EmailAddress

from users.forms import UserChangeForm, UserCreationForm
from users.models import User


class EmailAddressInline(admin.TabularInline):
    model = EmailAddress
    extra = 0


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    change_form_template = "admin/user_change_form.html"
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('id', 'email', 'username', 'password', 'token')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('last_login', 'date_joined', 'id', 'token')

    list_display = (
        'id', 'email', 'username', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'date_joined', 'last_login',
        'is_verified', 'is_email_verified'
    )
    list_display_links = ('email',)
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    actions = ['verify']

    inlines = [EmailAddressInline]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if obj is not None:
                yield inline.get_formset(request, obj), inline

    def get_queryset(self, request):
        return super().get_queryset(request).annotate_is_email_verified()

    def is_email_verified(self, obj):  # pylint: disable=no-self-use
        return obj.is_email_verified

    is_email_verified.boolean = True

    @staticmethod
    def token(obj):
        return obj.auth_token.key

    def get_list_filter(self, request):
        return super().get_list_filter(request) + ('is_verified',)

    def verify(self, request, queryset):  # pylint: disable=no-self-use
        queryset.update(is_verified=True)

    verify.short_description = "Mark selected users as verified"

    def response_change(self, request, obj):
        if "_verify-user" in request.POST:  # pragma: no cover
            obj.is_verified = True
            obj.save()
            self.message_user(request, f"User {str(obj)} has been marked as verified")
            return self.response_post_save_change(request, obj)
        return super().response_change(request, obj)
