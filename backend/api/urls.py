from django.urls import path

from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('graph', views.GraphViewSet, base_name='graphs')
urlpatterns = router.urls
