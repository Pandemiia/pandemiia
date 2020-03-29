from django.views.generic.base import TemplateView
# from rest_framework import viewsets
# from .serializer import HospitalNeedSerializer
# from .models import HospitalNeedModel


class HomePageView(TemplateView):
    template_name = 'medsupport/index.html'

#
# class HospitalNeedRestView(viewsets.ModelViewSet):
#     queryset = HospitalNeedModel.objects.all().order_by('-last_edited_on')
#     serializer_class = HospitalNeedSerializer
