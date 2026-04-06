from django.urls import path

from shipping.views import ActiveShippingSettingsView, ShippingHealthView

urlpatterns = [
    path("health/", ShippingHealthView.as_view(), name="shipping-health"),
    path(
        "settings/active/",
        ActiveShippingSettingsView.as_view(),
        name="shipping-active-settings",
    ),
]
