from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('openapi', get_schema_view(
      title="Pandemiia",
      description="API for this project",
      version="1.0.0"
    ), name='openapi-schema'),
    path('api_docs/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    path('', include('medsupport.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
