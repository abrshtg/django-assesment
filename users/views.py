import requests
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from social_core.exceptions import AuthException

from .models import CustomUser
from .serializers import (
    UserSignupSerializer,
    UserLoginSerializer,
    PasswordResetRequestSerializer,
    PasswordChangeSerializer,
    SocialSignupSerializer,
    SocialLoginSerializer,
)


class UserSignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    @extend_schema(request=UserLoginSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            tokens = serializer.get_tokens(user)

            return Response(
                {"email": user.email, "role": user.role, "tokens": tokens},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(generics.CreateAPIView):
    serializer_class = PasswordResetRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response(
            {"detail": "Password reset link sent."}, status=status.HTTP_200_OK
        )


class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(email=serializer.validated_data["email"])
        return Response(
            {"detail": "Password has been reset successfully."},
            status=status.HTTP_200_OK,
        )


class SocialSignupView(generics.CreateAPIView):
    serializer_class = SocialSignupSerializer  # Use the serializer here

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        provider = serializer.validated_data["provider"]
        access_token = serializer.validated_data["access_token"]

        try:
            user = self.authenticate_user(provider, access_token)
            if user:
                return Response(
                    {"id": user.id, "email": user.email, "role": user.role},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"error": "Authentication failed."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except AuthException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def authenticate_user(self, provider, access_token):
        """Authenticate the user using social-auth"""
        backend = (
            f"social_core.backends.{provider.lower()}.{provider.capitalize()}OAuth2"
        )

        # Use the logic for getting user details from the provider
        user_data = self.get_user_data(backend, access_token)

        if user_data:
            email = user_data.get("email")
            # Check if user already exists or create a new one
            user, created = CustomUser.objects.get_or_create(email=email)
            return user
        return None

    def get_user_data(self, backend, access_token):
        """Get user data from the social provider"""
        if backend == "social_core.backends.google.GoogleOAuth2":
            user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
            response = requests.get(
                user_info_url, headers={"Authorization": f"Bearer {access_token}"}
            )
            if response.status_code == 200:
                return response.json()
        elif backend == "social_core.backends.facebook.FacebookOAuth2":
            user_info_url = "https://graph.facebook.com/me?fields=id,name,email"
            response = requests.get(
                user_info_url, params={"access_token": access_token}
            )
            if response.status_code == 200:
                return response.json()

        return {}


class SocialLoginView(generics.GenericAPIView):
    serializer_class = SocialLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        provider = serializer.validated_data["provider"]
        access_token = serializer.validated_data["access_token"]

        try:
            user_data = self.get_user_data(provider, access_token)
            if user_data is None:
                return Response(
                    {"error": "Invalid token or provider"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            email = user_data.get("email")
            user, created = CustomUser.objects.get_or_create(email=email)

            token = self.generate_token(user)

            return Response(
                {"id": user.id, "email": user.email, "token": token},
                status=status.HTTP_200_OK,
            )

        except AuthException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_user_data(self, provider, access_token):
        if provider == "google":
            user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
            response = requests.get(
                user_info_url, headers={"Authorization": f"Bearer {access_token}"}
            )
        elif provider == "facebook":
            user_info_url = "https://graph.facebook.com/me?fields=id,name,email"
            response = requests.get(
                user_info_url, params={"access_token": access_token}
            )
        else:
            return None

        if response.status_code == 200:
            return response.json()
        return None

    def generate_token(self, user):
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
