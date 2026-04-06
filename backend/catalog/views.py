from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Product
from common.response import build_envelope


class CatalogHealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            build_envelope(
                success=True,
                message="Catalog service is healthy",
                data={"service": "catalog"},
                errors=None,
            )
        )


class ProductListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        products = list(
            Product.objects.filter(is_active=True)
            .order_by("-created_at")
            .values("id", "name", "slug", "price", "stock_quantity", "category_id")
        )
        return Response(
            build_envelope(
                success=True,
                message="Products fetched",
                data=products,
                errors=None,
            )
        )
