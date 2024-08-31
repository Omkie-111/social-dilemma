from django.db.models import Q
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model

from .serializers import (
    SignupSerializer,
    LoginSerializer,
    UserSerializer,
    FriendRequestSerializer,
)
from .models import FriendRequest

User = get_user_model()


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user": {"id": user.id, "email": user.email, "username": user.username},
            }
        )


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        query = self.request.query_params.get("q", "").strip().lower()
        return User.objects.filter(
            Q(email__iexact=query) | Q(username__icontains=query)
        )


class FriendRequestView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = {"sender": request.user.id, "receiver": request.data.get("receiver")}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer=serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FriendRequestActionView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        action = request.data.get("action")
        friend_request = self.get_object()
        print("hello")

        if action == "accept":
            if request.user != friend_request.receiver:
                raise PermissionDenied(
                    "You do not have permission to accept this friend request."
                )

            friend_request.is_accepted = True
            friend_request.save()
            return Response(status=status.HTTP_200_OK)

        elif action == "reject":
            friend_request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FriendListView(generics.ListAPIView):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(
            Q(
                sent_requests__receiver=self.request.user,
                sent_requests__is_accepted=True,
            )
            | Q(
                received_requests__sender=self.request.user,
                received_requests__is_accepted=True,
            )
        ).distinct()


class PendingRequestListView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(sender=self.request.user, is_accepted=False)
