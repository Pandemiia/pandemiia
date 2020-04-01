from django.urls import path
from .views import (
    HomePageView, PointRestView,
    NeedsRestView, CategoryPointRestView,
    CategoryArticleRestView,
)


urlpatterns = [
    path('category_article/', CategoryArticleRestView.as_view({'get': 'list'}), name='get-category-article'),
    path('category_point/', CategoryPointRestView.as_view({'get': 'list'}), name='get-category-points'),
    path('points/', PointRestView.as_view({'get': 'list'}), name='get-points'),
    path('short_points/', PointRestView.as_view({'get': 'list_short'}), name='get-short-points'),
    path('points/<int:pk>', PointRestView.as_view({'get': 'retrieve'}), name='get-single-point'),
    path('needs/', NeedsRestView.as_view({'get': 'list'}), name='get-needs'),
    path('', HomePageView.as_view(), name='index'),
]
