from django.contrib.auth.hashers import make_password
from rest_framework import serializers

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
