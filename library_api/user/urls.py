from django.urls import path
from .views import CustomTokenObtainPairView,UserRegistrationApiView,UserDetailsView,UserLibraryDetailsView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("", UserDetailsView.as_view(), name="user_details"),
    path("<int:library_id>/", UserLibraryDetailsView.as_view(), name="user_detail_for_library"),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("signup/", UserRegistrationApiView.as_view(), name='user_registration'),


]