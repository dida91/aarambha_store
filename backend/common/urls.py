from django.urls import path

from common.views import AdminMetricsView, CommonHealthView

urlpatterns = [
    path("health/", CommonHealthView.as_view(), name="common-health"),
    path("admin-metrics/", AdminMetricsView.as_view(), name="common-admin-metrics"),
]
