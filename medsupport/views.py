from django.views.generic.base import TemplateView
from rest_framework import viewsets
from .serializer import PointsSerializer, NeedsSerializer, PointsShortSerializer, PointDetailedSerializer, \
    CategoryPointSerializer, CategoryArticleSerializer
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

