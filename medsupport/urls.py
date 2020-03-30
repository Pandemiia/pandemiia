from django.urls import path
from .views import HomePageView, PointRestView, NeedsRestView, PointsShortRestView, PointDetailRestView


urlpatterns = [
    path('points/', PointRestView.as_view({'get': 'list'}), name='get-points'),
    path('points/<int:id>', PointDetailRestView.as_view({'get': 'list'}), name='get-singe-point'),
    path('short_points/', PointsShortRestView.as_view({'get': 'list'}), name='get-short-points'),
    path('needs/', NeedsRestView.as_view({'get': 'list'}), name='get-needs'),
    path('', HomePageView.as_view(), name='index'),
]
