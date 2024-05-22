from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views



urlpatterns = [
    path('users/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('users/signup/', views.RegisterUserView.as_view(), name='signup')
]