from django.utils.translation import gettext as _

from rest_auth.registration.views import VerifyEmailView as BaseVerifyEmailView
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.serializers import EmailVerificationSerializer


class ResendVerificationEmailView(GenericAPIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_email()
        return Response(data={"status": _("Email was re-send")}, status=status.HTTP_200_OK)


class VerifyEmailView(BaseVerifyEmailView):
    """
    Explicit declaration of this view is a workaround.
    Because endpoint `/verify-email/` fails on GET method because of redundant
    declaration of allowed HTTP methods in `VerifyEmailView` via `attribute allowed_methods`.
    https://github.com/Tivix/django-rest-auth/issues/581
    """
    http_method_names = [verb.lower() for verb in BaseVerifyEmailView.allowed_methods]
