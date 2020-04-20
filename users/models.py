import datetime

from allauth.account.models import EmailAddress
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel
from users.utils import generate_random_username


class UserQuerySet(models.QuerySet):
    def annotate_is_email_verified(self):
        subquery = EmailAddress.objects.filter(email=models.OuterRef("email"),
                                               user_id=models.OuterRef("id"),
                                               verified=True)
        return self.annotate(is_email_verified=models.Exists(subquery))


class UserManager(BaseUserManager):
    def get_queryset(self):
        return UserQuerySet(self.model)

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_verified', True)

        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    is_verified = models.BooleanField(_('is verified by admin'), default=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.set_username()
        super().save(*args, **kwargs)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def set_username(self):
        while True:
            username = generate_random_username(first_name=self.first_name, last_name=self.last_name, email=self.email)
            if not User.objects.filter(username=username).exists():  # pragma: no cover
                self.username = username
                break
