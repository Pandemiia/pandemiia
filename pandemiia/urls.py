"""pandemiia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
