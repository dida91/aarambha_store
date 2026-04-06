from django.urls import path

from accounts.views import AarambhaTokenObtainPairView, AarambhaTokenRefreshView, MeView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', AarambhaTokenObtainPairView.as_view(), name='login'),
    path('refresh/', AarambhaTokenRefreshView.as_view(), name='refresh'),
    path('me/', MeView.as_view(), name='me'),
]
