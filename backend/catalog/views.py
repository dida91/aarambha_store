from django.db.models import Prefetch
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from catalog.models import Category, Product, ProductImage
from catalog.serializers import CategorySerializer, ProductSerializer
from common.permissions import IsSellerOrAdmin
from common.response import build_envelope


class CatalogHealthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["get"], url_path="health")
    def health(self, request):
        return Response(
            build_envelope(
                success=True,
                message="Aarambha Store catalog service is healthy",
                data={"service": "catalog", "brand": "Aarambha Store"},
                errors=None,
            )
        )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in {"list", "retrieve"}:
            return [permissions.AllowAny()]
        return [IsSellerOrAdmin()]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True,
                message="Categories fetched",
                data=response.data,
                errors=None,
            )
        )

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True,
                message="Category fetched",
                data=response.data,
                errors=None,
            )
        )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True,
                message="Category created",
                data=response.data,
                errors=None,
            ),
            status=response.status_code,
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True,
                message="Category updated",
                data=response.data,
                errors=None,
            ),
            status=response.status_code,
        )

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True, message="Category deleted", data=None, errors=None
            ),
            status=response.status_code,
        )


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filterset_fields = ["category", "is_active"]
    search_fields = ["name", "description", "slug"]
    ordering_fields = ["created_at", "price", "name"]

    def get_queryset(self):
        queryset = Product.objects.select_related("category").prefetch_related(
            Prefetch(
                "images", queryset=ProductImage.objects.order_by("-is_primary", "id")
            )
        )
        if self.action in {"list", "retrieve"} and not (
            self.request.user.is_authenticated
            and (
                self.request.user.is_superuser
                or self.request.user.role in {"SELLER", "ADMIN"}
            )
        ):
            queryset = queryset.filter(is_active=True)
        return queryset

    def get_permissions(self):
        if self.action in {"list", "retrieve"}:
            return [permissions.AllowAny()]
        return [IsSellerOrAdmin()]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True,
                message="Products fetched",
                data=response.data,
                errors=None,
            )
        )

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True, message="Product fetched", data=response.data, errors=None
            )
        )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True, message="Product created", data=response.data, errors=None
            ),
            status=response.status_code,
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True, message="Product updated", data=response.data, errors=None
            ),
            status=response.status_code,
        )

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True, message="Product deleted", data=None, errors=None
            ),
            status=response.status_code,
        )
