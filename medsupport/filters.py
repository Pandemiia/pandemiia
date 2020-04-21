from django_filters import filters
from django_filters.rest_framework import FilterSet

from medsupport.models import Hospital
from medsupport.choices import REGION_CHOICES


class HospitalFilterSet(FilterSet):
    categories_in = filters.CharFilter(method='filter_categories_in')

    class Meta:
        model = Hospital
        fields = (
            'region',
            'categories_in'
        )

    def filter_categories_in(self, queryset, name, value):
        try:
            return queryset.filter(categories__in=value.split(',')).distinct()
        except ValueError:
            # Happens when non-decimal data is provided in value
            return queryset

