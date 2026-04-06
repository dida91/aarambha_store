from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from common.response import build_envelope

User = get_user_model()


class AccountsHealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            build_envelope(
                success=True,
                message="Accounts service is healthy",
                data={"service": "accounts"},
                errors=None,
            )
        )


class UserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = list(
            User.objects.order_by("id").values(
                "id", "username", "email", "role", "is_active"
            )
        )
        return Response(
            build_envelope(
                success=True,
                message="Users fetched",
                data=users,
                errors=None,
            )
        )
