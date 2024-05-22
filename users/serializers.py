from .models import User
from rest_framework.serializers import ModelSerializer


class UserRegisterSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["username", 'email', 'password']