from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import FriendRequest

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ["email", "password", "username", "first_name", "last_name", "phone"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone=validated_data["phone"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email").lower()
        password = data.get("password")
        user = authenticate(email=email, password=password)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid login credentials.")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username"]
        
        
class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'is_accepted', 'created_at']
        
    def validate(self, data):
        if FriendRequest.objects.filter(sender=data['sender'], receiver=data['receiver']).exists():
            raise serializers.ValidationError("Friend request already sent.")
        return data
