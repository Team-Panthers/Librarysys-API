from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from users.serializers import UserRegisterSerializer


class RegisterUserView(CreateAPIView):
    serializer_class = UserRegisterSerializer