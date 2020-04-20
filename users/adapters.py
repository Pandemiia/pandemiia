from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest, HttpResponseRedirect

from users.utils import generate_random_username


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

    # def get_email_confirmation_url(self, request, emailconfirmation):
    #     args = f"key={emailconfirmation.key}"
    #     return f"{settings.DJANGO_FRONTEND_EMAIL_CONFIRMATION_URL}?{args}"

    def generate_unique_username(self, txts, regex=None):
        return generate_random_username(first_name=txts[0], last_name=txts[1], email=txts[2])

    def respond_email_verification_sent(self, request, user):
        return HttpResponseRedirect('/')


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)
