from django.urls import path

from common.views import AdminDashboardMetricsView

urlpatterns = [
    path(
        "dashboard/metrics/",
        AdminDashboardMetricsView.as_view(),
        name="dashboard-metrics",
    ),
]
