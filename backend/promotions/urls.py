from django.urls import path

from promotions.views import PromoListView, PromotionsHealthView

urlpatterns = [
    path("health/", PromotionsHealthView.as_view(), name="promotions-health"),
    path("codes/", PromoListView.as_view(), name="promotions-codes"),
]
