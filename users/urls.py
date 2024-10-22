from django.urls import path

from .views import UserSignupView

urlpatterns = [
    path("users/signup/", UserSignupView.as_view(), name="user-signup"),
]
