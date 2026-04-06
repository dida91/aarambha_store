from django.urls import path

from common.views import CommonHealthView

urlpatterns = [
    path("health/", CommonHealthView.as_view(), name="common-health"),
]
