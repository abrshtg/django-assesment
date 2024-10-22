from django.urls import path

from .views import UserSignupView, UserLoginView

urlpatterns = [
    path("users/signup/", UserSignupView.as_view(), name="user-signup"),
    path("users/login/", UserLoginView.as_view(), name="user-login"),
]
