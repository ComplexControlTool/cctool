from django.urls import include, path

from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('graph', views.GraphViewSet, base_name='graphs')

urlpatterns = [
    path('', include(router.urls)),
    path('analysis/', views.GraphAnalysisList.as_view()),
]
