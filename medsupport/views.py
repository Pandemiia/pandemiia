from django.views.generic.base import TemplateView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializer import (
    PointsSerializer, NeedsSerializer, PointShortSerializer,
    PointDetailedSerializer, PointCategorySerializer, CategoryArticleSerializer,
)
from .models import PointModel, NeedModel, CategoryPointModel, CategoryArticleModel


class HomePageView(TemplateView):
    template_name = 'medsupport/index.html'


class CategoryArticleRestView(viewsets.ModelViewSet):
    """
        Returns a list with all Category of Articles
    """
    queryset = CategoryArticleModel.objects.all()
    serializer_class = CategoryArticleSerializer


class PointViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PointModel.objects.all()
    serializer_class = PointDetailedSerializer

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return PointDetailedSerializer
        if self.action in ['list_short']:
            return PointShortSerializer
        return PointsSerializer

    @action(methods=['GET'], detail=False, url_path='short')
    def list_short(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: PointCategorySerializer(many=True)})
    @action(methods=['GET'], detail=False)
    def categories(self, request, *args, **kwargs):
        qs = CategoryPointModel.objects.all()
        serializer = PointCategorySerializer(qs, many=True)
        return Response(serializer.data, status=200)


class NeedsRestView(viewsets.ModelViewSet):
    """
        Returns a list with all Needs
    """
    queryset = NeedModel.objects.all()
    serializer_class = NeedsSerializer

