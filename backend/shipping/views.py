from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common.permissions import IsSellerOrAdmin
from common.response import build_envelope
from shipping.models import ShippingConfig
from shipping.serializers import ShippingConfigSerializer
from shipping.services import get_active_shipping_config


class ShippingHealthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        return Response(
            build_envelope(
                success=True,
                message="Aarambha Store shipping service is healthy",
                data={"service": "shipping", "brand": "Aarambha Store"},
                errors=None,
            )
        )


class ShippingConfigViewSet(viewsets.ModelViewSet):
    queryset = ShippingConfig.objects.all().order_by("-created_at")
    serializer_class = ShippingConfigSerializer

    def get_permissions(self):
        if self.action in {"active", "calculate"}:
            return [permissions.AllowAny()]
        if self.action in {"list", "retrieve"}:
            return [permissions.IsAuthenticated()]
        return [IsSellerOrAdmin()]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True,
                message="Shipping configs fetched",
                data=response.data,
                errors=None,
            )
        )

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True,
                message="Shipping config fetched",
                data=response.data,
                errors=None,
            )
        )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True,
                message="Shipping config created",
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
                message="Shipping config updated",
                data=response.data,
                errors=None,
            ),
            status=response.status_code,
        )

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True, message="Shipping config deleted", data=None, errors=None
            ),
            status=response.status_code,
        )

    @action(detail=False, methods=["get"], url_path="active")
    def active(self, request):
        config = get_active_shipping_config()
        data = self.get_serializer(config).data
        return Response(
            build_envelope(
                success=True,
                message="Active shipping config fetched",
                data=data,
                errors=None,
            )
        )

    @action(detail=False, methods=["get"], url_path="calculate")
    def calculate(self, request):
        zone = request.query_params.get("zone", ShippingConfig.Zone.INSIDE_VALLEY)
        config = get_active_shipping_config()
        fee = config.calculate_delivery_fee(zone=zone)
        return Response(
            build_envelope(
                success=True,
                message="Shipping fee calculated",
                data={"zone": zone, "fee": fee},
                errors=None,
            )
        )
