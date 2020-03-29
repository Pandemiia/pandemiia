from django.urls import path
from .views import HomePageView #HospitalNeedRestView


urlpatterns = [
#    path('get_need/', HospitalNeedRestView.as_view({'get': 'list'}), name='get-need'),
    path('', HomePageView.as_view(), name='index'),
]
