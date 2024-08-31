from django.urls import path
from .views import SignupView, LoginView, UserSearchView, FriendRequestView, FriendRequestActionView, FriendListView, PendingRequestListView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("search/", UserSearchView.as_view(), name="user-search"),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('friend-request-action/<int:pk>/', FriendRequestActionView.as_view(), name='friend-request-action'),
    path('friends/', FriendListView.as_view(), name='friend-list'),
    path('pending-requests/', PendingRequestListView.as_view(), name='pending-requests'),
]
