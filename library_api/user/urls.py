from django.urls import path
from .views import CustomTokenObtainPairView,UserRegistrationApiView,UserDetailsView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("", UserDetailsView.as_view(), name="user_details"),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("signup/", UserRegistrationApiView.as_view(), name='user_registration')


]