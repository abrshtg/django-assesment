from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "role", "date_joined"]


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    # password = serializers.CharField(write_only=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "role", "password", "password_confirmation"]
        # extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):

        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):

        validated_data.pop("password_confirmation")
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise serializers.ValidationError("Invalid email or password.")
            if not user.is_active:
                raise serializers.ValidationError("This account is inactive.")

            data["user"] = user
        else:
            raise serializers.ValidationError("Both email and password are required.")

        return data

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
