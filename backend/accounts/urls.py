from django.urls import path

from accounts.views import AccountsHealthView, UserListView

urlpatterns = [
    path("health/", AccountsHealthView.as_view(), name="accounts-health"),
    path("users/", UserListView.as_view(), name="accounts-users"),
]
