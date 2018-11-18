from django.urls import path

from cctool.dashboard.views import (
    dashboard_page_view,
)

app_name = "dashboard"
urlpatterns = [
    path("", view=dashboard_page_view, name="dashboard"),
    path("graphs", view=dashboard_page_view, name="graphs"),
    path("graphs/<int:id>", view=dashboard_page_view, name="graphs_graph"),
    path("graphs/demo", view=dashboard_page_view, name="demos"),
    path("graphs/demo/<int:id>", view=dashboard_page_view, name="demos_demo"),
    path("graphs/new", view=dashboard_page_view, name="new"),
    path("graphs/new/create", view=dashboard_page_view, name="new_create"),
    path("graphs/new/import", view=dashboard_page_view, name="new_import"),
    path("graphs/edit", view=dashboard_page_view, name="edits"),
    path("graphs/edit/<int:id>", view=dashboard_page_view, name="edits_edit"),
    path("new_graph", view=dashboard_page_view, name="new_graph"),
    path("new_graph/create", view=dashboard_page_view, name="new_graph_create"),
    path("new_graph/import", view=dashboard_page_view, name="new_graph_import"),
    path("update_graph", view=dashboard_page_view, name="update_graph"),
    path("compare_graphs", view=dashboard_page_view, name="compare_graphs"),
    path("admin/graphs", view=dashboard_page_view, name="admin_graphs"),
]
