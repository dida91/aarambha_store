from django.urls import include, path
from rest_framework.routers import DefaultRouter

from catalog.views import CatalogHealthViewSet, CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register("health", CatalogHealthViewSet, basename="catalog-health")
router.register("categories", CategoryViewSet, basename="catalog-categories")
router.register("products", ProductViewSet, basename="catalog-products")

urlpatterns = [path("", include(router.urls))]
