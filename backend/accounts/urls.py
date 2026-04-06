from django.urls import path

from accounts.views import (
    AccountsHealthView,
    EnvelopedTokenObtainPairView,
    EnvelopedTokenRefreshView,
    ProfileView,
    RegisterView,
    UserListView,
)

urlpatterns = [
    path("health/", AccountsHealthView.as_view(), name="accounts-health"),
    path("register/", RegisterView.as_view(), name="accounts-register"),
    path("login/", EnvelopedTokenObtainPairView.as_view(), name="accounts-login"),
    path("refresh/", EnvelopedTokenRefreshView.as_view(), name="accounts-refresh"),
    path("me/", ProfileView.as_view(), name="accounts-me"),
    path("users/", UserListView.as_view(), name="accounts-users"),
]
