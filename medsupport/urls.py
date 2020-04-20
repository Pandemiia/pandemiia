from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (
    HomePageView,
    NeedsRestView,
    CategoryArticleRestView,
    PointViewSet
)

router = SimpleRouter()
router.register(r'points', PointViewSet)

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('category_article/', CategoryArticleRestView.as_view({'get': 'list'}), name='get-category-article'),
    path('needs/', NeedsRestView.as_view({'get': 'list'}), name='get-needs'),
] + router.urls
