from django_filters import filters
from django_filters.rest_framework import FilterSet

from medsupport.models import Hospital, Solution, SolutionCategory


# BaseInFilter let us provide comma separated values for OR filtering


class HospitalFilterSet(FilterSet):
    needs_categories = filters.BaseInFilter(
        field_name='needs__solution_type__solutions__categories',
    )
    categories = filters.BaseInFilter()
    region = filters.BaseInFilter()

    class Meta:
        model = Hospital
        fields = (
            'region',
            'categories',
            'needs_categories',
        )


class SolutionFilterSet(FilterSet):
    solution_type = filters.BaseInFilter()
    materials = filters.BaseInFilter()
    tools = filters.BaseInFilter()

    class Meta:
        model = Solution
        fields = (
            'solution_type',
            'materials',
            'tools',
        )
