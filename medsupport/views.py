from django.views.generic.base import TemplateView
from rest_framework import viewsets
from rest_framework.decorators import action

from .serializer import (
    PointsSerializer, NeedsSerializer, PointsShortSerializer,
    PointDetailedSerializer, CategoryPointSerializer, CategoryArticleSerializer,
)
from .models import PointModel, NeedModel, CategoryPointModel, CategoryArticleModel


class HomePageView(TemplateView):
    template_name = 'medsupport/index.html'


class CategoryPointRestView(viewsets.ModelViewSet):
    """
        Returns a list with all Category of Points
    """
    queryset = CategoryPointModel.objects.all()
    serializer_class = CategoryPointSerializer


class CategoryArticleRestView(viewsets.ModelViewSet):
    """
        Returns a list with all Category of Articles
    """
    queryset = CategoryArticleModel.objects.all()
    serializer_class = CategoryArticleSerializer



class PointRestView(viewsets.ModelViewSet):
    """
        Point view set
    """
    queryset = PointModel.objects.all()
    serializer_class = PointDetailedSerializer

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return PointDetailedSerializer
        if self.action in ['list_short']:
            return PointsShortSerializer
        return PointsSerializer

    @action(methods=['GET'], detail=False)
    def list_short(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class NeedsRestView(viewsets.ModelViewSet):
    """
        Returns a list with all Needs
    """
    queryset = NeedModel.objects.all()
    serializer_class = NeedsSerializer

