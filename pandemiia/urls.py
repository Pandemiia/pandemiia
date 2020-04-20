from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('medsupport.urls')),
    path('', include('users.urls')),
]

# Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Pandemiia API",
        default_version='v1',
        # description="Test description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)
urlpatterns += [
    path('api_docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
