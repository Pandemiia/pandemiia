from django.views.generic.base import TemplateView
from rest_framework import viewsets
from .serializer import PointsSerializer, NeedsSerializer, PointsShortSerializer, PointDetailedSerializer
from .models import PointModel, NeedModel


class HomePageView(TemplateView):
    template_name = 'medsupport/index.html'


class PointRestView(viewsets.ModelViewSet):
    """
        Returns a list with all Points
    """
    queryset = PointModel.objects.all()
    serializer_class = PointsSerializer


class PointsShortRestView(viewsets.ModelViewSet):
    """
        Returns a short list with all Points
    """
    queryset = PointModel.objects.all()
    serializer_class = PointsShortSerializer


class PointDetailRestView(viewsets.ModelViewSet):
    """
        Returns a single Point object
    """
    queryset = PointModel.objects.all()
    serializer_class = PointDetailedSerializer

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs.get('id'))


class NeedsRestView(viewsets.ModelViewSet):
    """
        Returns a list with all Needs
    """
    queryset = NeedModel.objects.all()
    serializer_class = NeedsSerializer

