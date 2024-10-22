from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import (
    UserSignupSerializer,
    UserLoginSerializer,
    PasswordResetRequestSerializer,
    PasswordChangeSerializer,
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
