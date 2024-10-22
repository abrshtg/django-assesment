from django.urls import path

from .views import (
    UserSignupView,
    UserLoginView,
    PasswordResetRequestView,
    PasswordChangeView,
    SocialSignupView,
)

urlpatterns = [
    path("users/signup/", UserSignupView.as_view(), name="user-signup"),
    path("users/login/", UserLoginView.as_view(), name="user-login"),
    path(
        "users/password-reset/",
        PasswordResetRequestView.as_view(),
        name="password-reset",
    ),
    path(
        "users/password-change/", PasswordChangeView.as_view(), name="password-change"
    ),
    path("users/social-signup/", SocialSignupView.as_view(), name="social-signup"),
]
