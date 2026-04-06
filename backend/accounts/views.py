from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.serializers import RegisterSerializer, UserSerializer
from common.permissions import IsSellerOrAdmin
from common.response import build_envelope

User = get_user_model()


class EnvelopedTokenObtainPairView(TokenObtainPairView):
    throttle_scope = "auth"

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True,
                message="Login successful",
                data=response.data,
                errors=None,
            ),
            status=response.status_code,
        )


class EnvelopedTokenRefreshView(TokenRefreshView):
    throttle_scope = "auth"

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True,
                message="Token refreshed",
                data=response.data,
                errors=None,
            ),
            status=response.status_code,
        )


class AccountsHealthView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(
            build_envelope(
                success=True,
                message="Aarambha Store accounts service is healthy",
                data={"service": "accounts", "brand": "Aarambha Store"},
                errors=None,
            )
        )


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_scope = "auth"

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True,
                message="Registration successful",
                data=response.data,
                errors=None,
            ),
            status=response.status_code,
        )


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(
            build_envelope(
                success=True,
                message="Profile fetched",
                data=UserSerializer(request.user).data,
                errors=None,
            )
        )


class UserListView(generics.ListAPIView):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    permission_classes = [IsSellerOrAdmin]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            build_envelope(
                success=True,
                message="Users fetched",
                data=response.data,
                errors=None,
            )
        )
