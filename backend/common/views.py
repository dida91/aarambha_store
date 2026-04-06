from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from common.response import build_envelope


class CommonHealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            build_envelope(
                success=True,
                message="Common service is healthy",
                data={"service": "common"},
                errors=None,
            )
        )
