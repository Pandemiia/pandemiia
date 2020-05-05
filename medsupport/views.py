from django.db.models import Count, Q
from django.views.generic.base import TemplateView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .choices import REGION_CHOICES
from .filters import HospitalFilterSet, SolutionFilterSet
from .serializers import (
    HospitalSerializer, HospitalNeedSerializer,
    HospitalDetailedSerializer,
    HospitalCategorySerializer, SolutionCategorySerializer,
    SolutionSerializer, SolutionMaterialsSerializer,
    SolutionToolsSerializer, SolutionTypeSerializer,
    HospitalRegionsSerializer
)
from .models import (
    Hospital, HospitalNeed,
    HospitalCategory, SolutionCategory,
    Solution, Material, Tool,
    SolutionType,
)


class HomePageView(TemplateView):
    template_name = 'medsupport/index.html'


class HospitalsViewSet(ReadOnlyModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalDetailedSerializer
    filterset_class = HospitalFilterSet

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return HospitalDetailedSerializer
        return HospitalSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.distinct()

    @swagger_auto_schema(responses={200: HospitalCategorySerializer(many=True)})
    @action(methods=['GET'], detail=False)
    def categories(self, request, *args, **kwargs):
        qs = HospitalCategory.objects.all()
        serializer = HospitalCategorySerializer(qs, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(responses={200: SolutionCategorySerializer(many=True)})
    @action(methods=['GET'], detail=False, url_path='needs-categories')
    def needs_categories(self, request, *args, **kwargs):
        qs = SolutionCategory.objects.all()
        serializer = SolutionCategorySerializer(qs, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(responses={200: HospitalRegionsSerializer(many=True)})
    @action(methods=['GET'], detail=False)
    def regions(self, request, *args, **kwargs):
        # Count all hospitals by region in one request to db
        # -> {region_key_1: amount_1, region_key_n: amount_n}
        hospitals_counted_by_region = Hospital.objects.aggregate(
            **{str(region_key): Count('pk', filter=Q(region=region_key))
               for region_key, _ in REGION_CHOICES}
        )
        data = [
            {'key': key,
             'name': name,
             'hospitals_in_region': hospitals_counted_by_region[str(key)]}
            for key, name in REGION_CHOICES
        ]
        serializer = HospitalRegionsSerializer(data, many=True)
        return Response(serializer.data, status=200)


class HospitalNeedsViewSet(ReadOnlyModelViewSet):
    queryset = HospitalNeed.objects.all()
    serializer_class = HospitalNeedSerializer


class SolutionsViewSet(ReadOnlyModelViewSet):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    filterset_class = SolutionFilterSet

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.distinct()

    @swagger_auto_schema(responses={200: SolutionTypeSerializer(many=True)})
    @action(methods=['GET'], detail=False)
    def type(self, request, *args, **kwargs):
        qs = SolutionType.objects.all()
        serializer = SolutionTypeSerializer(qs, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(responses={200: SolutionCategorySerializer(many=True)})
    @action(methods=['GET'], detail=False)
    def categories(self, request, *args, **kwargs):
        qs = SolutionCategory.objects.all()
        serializer = SolutionCategorySerializer(qs, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(responses={200: SolutionMaterialsSerializer(many=True)})
    @action(methods=['GET'], detail=False)
    def materials(self, request, *args, **kwargs):
        qs = Material.objects.all()
        serializer = SolutionMaterialsSerializer(qs, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(responses={200: SolutionToolsSerializer(many=True)})
    @action(methods=['GET'], detail=False)
    def tools(self, request, *args, **kwargs):
        qs = Tool.objects.all()
        serializer = SolutionToolsSerializer(qs, many=True)
        return Response(serializer.data, status=200)


