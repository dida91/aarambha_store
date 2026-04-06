from django.urls import path

from catalog.views import CatalogHealthView, ProductListView

urlpatterns = [
    path("health/", CatalogHealthView.as_view(), name="catalog-health"),
    path("products/", ProductListView.as_view(), name="catalog-products"),
]
