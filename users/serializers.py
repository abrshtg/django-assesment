from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
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

    class Meta:
        model = CustomUser
        fields = ["id", "email", "role", "password", "password_confirmation"]

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


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("No user is associated with this email.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.get(email=validated_data["email"])

        token = default_token_generator.make_token(user)

        send_mail(
            "Password Reset",
            f"Your password reset token is: {token}\nUse this token to reset your password.",
            "from@example.com",
            [user.email],
            fail_silently=False,
        )
        return validated_data


from django.contrib.auth.tokens import default_token_generator


class PasswordChangeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):

        user = CustomUser.objects.filter(email=data["email"]).first()
        if user is None or not default_token_generator.check_token(user, data["token"]):
            raise serializers.ValidationError("Invalid token.")

        if len(data["new_password"]) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )

        return data

    def save(self, **kwargs):

        email = kwargs.get("email")
        user = CustomUser.objects.get(email=email)
        user.set_password(self.validated_data["new_password"])
        user.save()


class SocialSignupSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=["google", "facebook"])
    access_token = serializers.CharField()


class SocialLoginSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=["google", "facebook"])
    access_token = serializers.CharField()
