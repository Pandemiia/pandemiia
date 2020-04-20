from django.contrib.auth import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from users.models import User


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):
    error_message = forms.UserCreationForm.error_messages.update({
        'duplicate_email': _('This email has already been taken.')
    })

    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(self.error_messages['duplicate_email'])
        return email
