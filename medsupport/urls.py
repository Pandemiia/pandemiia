from django.urls import path
from .views import HomePageView, PointRestView


urlpatterns = [
   path('points/', PointRestView.as_view({'get': 'list'}), name='get-need'),
    path('', HomePageView.as_view(), name='index'),
]
