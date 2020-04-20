from django.views.generic.base import TemplateView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import (
    HospitalSerializer, HospitalNeedSerializer,
    HospitalShortSerializer, HospitalDetailedSerializer,
    HospitalCategorySerializer, SolutionCategorySerializer,
    SolutionSerializer,
)
from .models import (
    Hospital, HospitalNeed,
    HospitalCategory, SolutionCategory,
    Solution,
)


class HomePageView(TemplateView):
    template_name = 'medsupport/index.html'


class HospitalsViewSet(ReadOnlyModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalDetailedSerializer
    filterset_fields = ('region', 'categories')

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return HospitalDetailedSerializer
        if self.action in ['list_short']:
            return HospitalShortSerializer
        return HospitalSerializer

    @action(methods=['GET'], detail=False, url_path='list-short')
    def list_short(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: HospitalCategorySerializer(many=True)})
    @action(methods=['GET'], detail=False)
    def categories(self, request, *args, **kwargs):
        qs = HospitalCategory.objects.all()
        serializer = HospitalCategorySerializer(qs, many=True)
        return Response(serializer.data, status=200)


class HospitalNeedsViewSet(ReadOnlyModelViewSet):
    queryset = HospitalNeed.objects.all()
    serializer_class = HospitalNeedSerializer


class SolutionsViewSet(ReadOnlyModelViewSet):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer

    @swagger_auto_schema(responses={200: SolutionCategorySerializer(many=True)})
    @action(methods=['GET'], detail=False)
    def categories(self, request, *args, **kwargs):
        qs = SolutionCategory.objects.all()
        serializer = SolutionCategorySerializer(qs, many=True)
        return Response(serializer.data, status=200)

