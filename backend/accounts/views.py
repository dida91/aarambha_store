from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.serializers import AarambhaTokenSerializer, RegisterSerializer, UserSerializer
from common.response import api_response


class RegisterView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

    def post(self, request):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return api_response(
            message='User registered successfully.',
            data=UserSerializer(user).data,
            http_status=status.HTTP_201_CREATED,
        )


class AarambhaTokenObtainPairView(TokenObtainPairView):
    serializer_class = AarambhaTokenSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return api_response(message='Login successful.', data=response.data)


class AarambhaTokenRefreshView(TokenRefreshView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return api_response(message='Token refreshed.', data=response.data)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return api_response(data=UserSerializer(request.user).data)
