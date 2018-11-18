from django.urls import path

from cctool.dashboard.views import (
    dashboard_page_view,
)

app_name = "cctool"
urlpatterns = [
    path("", view=dashboard_page_view, name="dashboard"),
]
