
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics

from .serializers import CustomTokenObtainPairSerializer,UserRegistrationSerializer,UserSerializer


# Create your views here.


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRegistrationApiView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer


class UserDetailsView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
