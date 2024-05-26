
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import CustomTokenObtainPairSerializer,UserRegistrationSerializer,UserSerializer,UserSerializer2
from library_api.mixins import ConfirmLibraryDispatchMixin,LibraryContextMixin


# Create your views here.


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

class UserRegistrationApiView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserDetailsView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
class UserLibraryDetailsView(ConfirmLibraryDispatchMixin,LibraryContextMixin,generics.RetrieveAPIView):
    serializer_class = UserSerializer2

    def get_object(self):
        return self.request.user
