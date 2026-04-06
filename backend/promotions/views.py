from django.db import models
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from common.response import build_envelope
from promotions.models import PromoCode


class PromotionsHealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            build_envelope(
                success=True,
                message="Promotions service is healthy",
                data={"service": "promotions"},
                errors=None,
            )
        )


class PromoListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        now = timezone.now()
        promos = list(
            PromoCode.objects.filter(is_active=True)
            .filter(models.Q(starts_at__isnull=True) | models.Q(starts_at__lte=now))
            .filter(models.Q(ends_at__isnull=True) | models.Q(ends_at__gte=now))
            .values(
                "id",
                "code",
                "discount_type",
                "discount_value",
                "min_cart_value",
                "is_public",
            )
        )
        return Response(
            build_envelope(
                success=True,
                message="Promotions fetched",
                data=promos,
                errors=None,
            )
        )
