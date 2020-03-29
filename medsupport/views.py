from django.views.generic.base import TemplateView
from rest_framework import viewsets
from .serializer import PointSerializer
from .models import PointModel


class HomePageView(TemplateView):
    template_name = 'medsupport/index.html'

#
class PointRestView(viewsets.ModelViewSet):
    queryset = PointModel.objects.all()
    serializer_class = PointSerializer
