from decimal import Decimal

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common.permissions import IsSellerOrAdmin
from common.response import build_envelope
from promotions.models import PromoCode
from promotions.serializers import PromoCodeSerializer
from promotions.services import validate_and_calculate_discount


class PromotionsHealthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        return Response(
            build_envelope(
                success=True,
                message="Aarambha Store promotions service is healthy",
                data={"service": "promotions", "brand": "Aarambha Store"},
                errors=None,
            )
        )


class PromoCodeViewSet(viewsets.ModelViewSet):
    queryset = PromoCode.objects.prefetch_related("allowed_users").order_by(
        "-created_at"
    )
    serializer_class = PromoCodeSerializer
    filterset_fields = ["is_active", "is_public", "discount_type"]
    search_fields = ["code"]
    ordering_fields = ["created_at", "code", "used_count"]

    def get_permissions(self):
        if self.action in {"list", "retrieve", "validate"}:
            return [permissions.IsAuthenticated()]
        return [IsSellerOrAdmin()]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True,
                message="Promo codes fetched",
                data=response.data,
                errors=None,
            )
        )

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True,
                message="Promo code fetched",
                data=response.data,
                errors=None,
            )
        )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True,
                message="Promo code created",
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
                message="Promo code updated",
                data=response.data,
                errors=None,
            ),
            status=response.status_code,
        )

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True, message="Promo code deleted", data=None, errors=None
            ),
            status=response.status_code,
        )

    @action(detail=False, methods=["post"], url_path="validate")
    def validate(self, request):
        code = request.data.get("code")
        subtotal = Decimal(str(request.data.get("subtotal", "0")))
        discount, promo = validate_and_calculate_discount(
            user=request.user,
            code=code,
            subtotal=subtotal,
        )
        data = {
            "code": promo.code if promo else None,
            "discount": discount,
            "subtotal": subtotal,
            "total_after_discount": subtotal - discount,
        }
        return Response(
            build_envelope(
                success=True,
                message="Promo validated",
                data=data,
                errors=None,
            ),
            status=status.HTTP_200_OK,
        )
