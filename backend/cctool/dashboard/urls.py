from django.urls import path

from cctool.dashboard.views import (
    dashboard_page_view,
)

app_name = "dashboard"
urlpatterns = [
    path("", view=dashboard_page_view, name="dashboard"),
    path("graphs", view=dashboard_page_view, name="dashboard"),
    path("graphs/<int:id>", view=dashboard_page_view, name="dashboard"),
    path("graphs/demo", view=dashboard_page_view, name="dashboard"),
    path("graphs/demo/<int:id>", view=dashboard_page_view, name="dashboard"),
    path("graphs/new", view=dashboard_page_view, name="dashboard"),
    path("graphs/new/create", view=dashboard_page_view, name="dashboard"),
    path("graphs/new/import", view=dashboard_page_view, name="dashboard"),
    path("graphs/edit", view=dashboard_page_view, name="dashboard"),
    path("graphs/edit/<int:id>", view=dashboard_page_view, name="dashboard"),
    path("new_graph", view=dashboard_page_view, name="dashboard"),
    path("new_graph/create", view=dashboard_page_view, name="dashboard"),
    path("new_graph/import", view=dashboard_page_view, name="dashboard"),
    path("update_graph", view=dashboard_page_view, name="dashboard"),
    path("compare_graphs", view=dashboard_page_view, name="dashboard"),
    path("admin/graphs", view=dashboard_page_view, name="dashboard"),
]
