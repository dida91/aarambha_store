from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from common.response import build_envelope
from shipping.models import ShippingSettings


class ShippingHealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            build_envelope(
                success=True,
                message="Shipping service is healthy",
                data={"service": "shipping"},
                errors=None,
            )
        )


class ActiveShippingSettingsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        settings_obj = ShippingSettings.objects.filter(is_active=True).first()
        data = None
        if settings_obj:
            data = {
                "id": settings_obj.id,
                "inside_valley_fee": settings_obj.inside_valley_fee,
                "outside_valley_fee": settings_obj.outside_valley_fee,
                "free_inside_valley": settings_obj.free_inside_valley,
                "free_delivery_all_nepal": settings_obj.free_delivery_all_nepal,
            }

        return Response(
            build_envelope(
                success=True,
                message="Active shipping settings fetched",
                data=data,
                errors=None,
            )
        )
